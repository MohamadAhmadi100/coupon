from app.buying.add_imei import add_buying_imei, remove_buying_imei
from app.buying.edit_form import *
from app.buying.forms import create_form, wms_notification, logistic_confirm, submit_warehouse_products_buying
from app.buying.get_buying import *
from app.suppliers.add_supplier import add_supplier
from app.suppliers.edit_supplier import edit_supplier_root, edit_supplier_addresses
from app.suppliers.get_supplier import *

"""
suppliers
"""


def new_supplier(supplier_name, economic_code, state, status, supplier_type, supplier_level, website_url, telegram,
                 mobile_Number, kosar_id, office_address, store_address, supplier_variety):
    return add_supplier(supplier_name, economic_code, state, status, supplier_type, supplier_level, website_url,
                        telegram,
                        mobile_Number, kosar_id, office_address, store_address, supplier_variety)


def edit_supplier_detail(supplier_id, edited_data):
    return edit_supplier_root(supplier_id, edited_data)


def edit_supplier_address(address_id, store, edited_data):
    return edit_supplier_addresses(address_id, store, edited_data)


def supplier(supplier_id):
    return get_supplier(supplier_id)


def suppliers(page, perPage):
    return get_suppliers(page, perPage)


def suppliers_name():
    return get_suppliers_name()


"""
Buying
"""


def wms_buying_report(storage_id):
    try:
        return get_wms_buying_report(storage_id)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}


def wms_buying_list(storage_id, page, perPage):
    try:
        return get_wms_buying(storage_id, page, perPage)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}


def wms_buying_one(referral_number):
    try:
        return get_wms_buying_one(referral_number)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}


def scm_buying_forms(page, perPage, system_code, status, referral_number):
    try:
        return get_scm_buying_forms(page, perPage, system_code, status, referral_number)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}


def products_buying(referral_number):
    try:
        return get_products_buying(referral_number)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}


def add_imei_to_buying(referral_number, system_code, imei):
    try:
        return add_buying_imei(referral_number, system_code, imei)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}


def remove_imei_to_buying(referral_number, system_code, imei):
    try:
        return remove_buying_imei(referral_number, system_code, imei)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}


def create_buying_form(products, storage, supplier, payment_method, delivery_type, qty_type, cheques,
                       description, delivery_date, wms_notification, logistic_status):
    try:
        return create_form(products, storage, supplier, payment_method, delivery_type, qty_type, cheques,
                           description, delivery_date, wms_notification, logistic_status)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}


def buying_to_wms(referral_number):
    try:
        return wms_notification(referral_number)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}


def logistic_to_wms(referral_number):
    try:
        return logistic_confirm(referral_number)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}


def get_submit_warehouse_products_buying(referral_number, system_code):
    try:
        return get_warehouse_products_buying(referral_number, system_code)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}


def put_submit_warehouse_products_buying(referral_number, system_code):
    try:
        return submit_warehouse_products_buying(referral_number, system_code)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}


def delete_buying_product(referral_number, system_code):
    try:
        return delete_product(referral_number, system_code)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}


def add_buying_product(referral_number, system_code, count, name, brand, model, color, seller, guaranty,
                       unit_price, sell_price, GIN):
    try:
        return add_products(referral_number, system_code, count, name, brand, model, color, seller, guaranty, unit_price,
                           sell_price, GIN)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}


def edit_buying_product(referral_number, edited_product):
    try:
        return edit_products(referral_number, edited_product)
    except:
        return {"success": False, "error": "controller root exception", "status_code": 400}
