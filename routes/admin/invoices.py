from flask import Blueprint, render_template, request
from extensions import csrf


admin_invoices_bp = Blueprint('admin_invoices', __name__, url_prefix='/admin/invoices')

BUSINESS = {
    "name": "Nexus Diagnostics — Mobile Mechanic",
    "phone": "0437 133 718",
    "service_area": "Servicing Canberra & surrounds",
    "city_state": "Canberra ACT",
    "email": "nexusdiagnostics@busacker.xyz",
}


# ---------- HELPER: Split items into pages ----------
def paginate_items(items, items_per_page=8):
    """
    Split items into pages for multi-page invoices.
    Returns a dict with page data and total pages.
    """
    total_items = len(items)
    total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
    
    page_data = {}
    
    if total_items > 0:
        for page_num in range(1, total_pages + 1):
            start_idx = (page_num - 1) * items_per_page
            end_idx = min(page_num * items_per_page, total_items)
            page_data[f'items_page{page_num}'] = items[start_idx:end_idx]
        
        if total_pages > 1:
            page_data['items_last_page'] = items[(total_pages - 1) * items_per_page:]
        else:
            page_data['items_last_page'] = items
    else:
        page_data['items_page1'] = []
        page_data['items_last_page'] = []
        total_pages = 1
    
    return page_data, total_pages


@admin_invoices_bp.route('/', methods=["GET"])
def list_invoices():
    return render_template("admin/invoices/create.html", business=BUSINESS)


@csrf.exempt
@admin_invoices_bp.route("/", methods=["POST"])
def create_invoice():
    form = request.form

    # ---------- Business ----------
    business = {
        "name": form.get("business_name", ""),
        "phone": form.get("business_phone", ""),
        "service_area": form.get("business_service_area", ""),
        "city_state": form.get("business_city_state", ""),
        "email": form.get("business_email", ""),
    }

    # ---------- Customer ----------
    customer = {
        "code": form.get("customer_code", ""),
        "name": form.get("customer_name", ""),
        "address": [
            line.strip()
            for line in form.get("customer_address", "").splitlines()
            if line.strip()
        ],
    }

    # ---------- Invoice ----------
    invoice = {
        "type": form.get("invoice_type", ""),
        "title": form.get("invoice_title", ""),
        "number": form.get("invoice_number", ""),
    }

    # ---------- Job ----------
    job = {
        "issued": form.get("issued", ""),
        "technician": form.get("technician", ""),
        "finalised_by": form.get("finalised_by", ""),
        "customer_name": form.get("job_customer_name", ""),
    }

    # ---------- Vehicle ----------
    vehicle = {
        "make": form.get("vehicle_make", ""),
        "series": form.get("vehicle_series", ""),
        "year": form.get("vehicle_year", ""),
        "odometer": form.get("vehicle_odometer", ""),
        "model": form.get("vehicle_model", ""),
        "registration": form.get("vehicle_registration", ""),
        "vin": form.get("vehicle_vin", ""),
        "paid_by": form.get("paid_by", ""),
    }

    work_order = form.get("work_order", "")

    # ---------- Line Items & Notes ----------
    # Get all the arrays from the form
    item_types = form.getlist("item_type[]")
    products = form.getlist("item_product[]")
    descriptions = form.getlist("item_description[]")
    qtys = form.getlist("item_qty[]")
    prices = form.getlist("item_price[]")
    amounts = form.getlist("item_amount[]")
    note_texts = form.getlist("item_note_text[]")

    items = []
    item_details = {}  # Dict to store all line details with line numbers
    
    # Get the maximum length of all arrays
    max_len = max(len(item_types), len(products), len(descriptions), 
                  len(qtys), len(prices), len(amounts), len(note_texts))
    
    # Process each row
    for i in range(max_len):
        # Get item type, default to "item" if not set
        item_type = item_types[i] if i < len(item_types) else "item"
        
        if item_type == "note":
            # This is a standalone note
            note_text = note_texts[i].strip() if i < len(note_texts) else ""
            if note_text:  # Only add if there's actual text
                item_data = {
                    "line_number": i + 1,
                    "is_note": True,
                    "note_text": note_text,
                    "product": "",
                    "description": "",
                    "qty": "",
                    "price": "",
                    "amount": "",
                }
                items.append(item_data)
                item_details[f"line_{i+1}"] = item_data
        else:
            # This is a line item
            product = products[i].strip() if i < len(products) else ""
            description = descriptions[i].strip() if i < len(descriptions) else ""
            
            # Skip completely empty line items
            if not product and not description:
                continue
                
            item_data = {
                "line_number": i + 1,
                "is_note": False,
                "product": product,
                "description": description,
                "qty": qtys[i].strip() if i < len(qtys) else "",
                "price": prices[i].strip() if i < len(prices) else "",
                "amount": amounts[i].strip() if i < len(amounts) else "",
                "note_text": "",
            }
            items.append(item_data)
            item_details[f"line_{i+1}"] = item_data

    # ---------- Totals ----------
    total_labels = form.getlist("total_label[]")
    total_values = form.getlist("total_value[]")

    totals = []
    for i in range(len(total_labels)):
        label = total_labels[i].strip() if i < len(total_labels) else ""
        value = total_values[i].strip() if i < len(total_values) else ""
        if not label:
            continue
        # Check if this is the total row
        is_total = label.upper() in ["TOTAL", "TOTAL (INC GST)", "TOTAL INC GST"]
        totals.append({
            "label": label,
            "value": value,
            "total": is_total
        })

    # Get the final total from the form
    final_label = form.get("total_final_label", "Total").strip()
    final_value = form.get("total_final_value", "").strip()
    
    # Check if we already have a total row
    has_total = any(row.get("total", False) for row in totals)
    
    if final_label and final_value and not has_total:
        totals.append({
            "label": final_label, 
            "value": final_value, 
            "total": True
        })
    elif final_label and final_value and has_total:
        # Update the existing total row
        for row in totals:
            if row.get("total", False):
                row["value"] = final_value
                break

    # ---------- Bank Details ----------
    bank_data = {
        'account_name': form.get('bank_account_name', ''),
        'bsb': form.get('bank_bsb', ''),
        'account_number': form.get('bank_account_number', '')
    }

    # ---------- Footer ----------
    footer_note = form.get("footer_note", "")
    page_info = form.get("page_info", "")

    # ---------- Paginate Items ----------
    items_per_page = 8
    page_data, total_pages = paginate_items(items, items_per_page)

    # ---------- Build Context ----------
    context = {
        "business": business,
        "customer": customer,
        "invoice": invoice,
        "job": job,
        "vehicle": vehicle,
        "work_order": work_order,
        "items": items,  # Full list of items with line numbers
        "item_details": item_details,  # Dict with line_number as key
        "totals": totals,
        "bank": bank_data,
        "footer_note": footer_note,
        "page_info": page_info,
        "total_pages": total_pages,
        "page_data": page_data,
        **page_data,  # Unpacks items_page1, items_page2, items_last_page, etc.
    }

    return render_template("admin/invoices/template.html", **context)