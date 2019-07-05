# -*- coding: utf-8 -GPK*-

{
    "name": "Sivappu-Hospital",
    "version": "1.0",
    "author": "La Mars",
    "website": "http://",
    "category": "Sivappu_hospital",
    "sequence": 1,
    "summary": "Hospital Management System",
    "description": """

    Hospital Management System

    Patient Management
    Employee Management
    Purchase Management
    Pharmacy Management
    Assert Management
    Accounts Management

    """,
    "depends": ["base", "mail"],
    "data": [

        "views/assert_backend.xml",

        "security/security.xml",
        "security/base.xml",
        "security/billing.xml",
        "security/configuration.xml",
        "security/general.xml",
        "security/ipd.xml",
        "security/opd.xml",
        "security/operation.xml",
        "security/product.xml",
        "security/staff.xml",
        "security/stock.xml",
        "security/ward.xml",
        "security/ir.model.access.csv",

        "sequence/base.xml",
        "sequence/testing.xml",
        "sequence/am_hospital.xml",

        # Base
        "views/base/patient.xml",
        "views/base/staff.xml",
        "views/base/person.xml",

        # Contact
        "views/contact/contact.xml",
        "views/contact/patient.xml",
        "views/contact/staff.xml",
        "views/contact/supplier.xml",
        "views/contact/service.xml",

        # General

        # Reception
        "views/reception/doctor_availability.xml",
        "views/reception/doctor_timings.xml",
        "views/reception/notes.xml",
        "views/reception/reminder.xml",

        # OPD
        "views/opd/appointment.xml",
        "views/opd/general_treatment.xml",
        "views/opd/prescription.xml",
        "views/opd/clinical_notes.xml",

        # IPD
        "views/ipd/admission.xml",
        "views/ipd/ipd_treatment.xml",
        "views/ipd/prescription.xml",
        "views/ipd/discharge.xml",

        # Ward
        "views/ward/ward.xml",
        "views/ward/bed.xml",
        "views/ward/patient_shifting.xml",

        # Operation
        "views/operation/operation.xml",
        "views/operation/operation_theater.xml",
        "views/operation/patient_operation.xml",

        # Product
        "views/product/product.xml",
        "views/product/product_group.xml",
        "views/product/product_sub_group.xml",
        "views/product/location.xml",

        # Stock
        "views/stock/batch.xml",
        "views/stock/stock_adjust.xml",
        "views/stock/stock_block.xml",
        "views/stock/stock_scrap.xml",
        "views/stock/stock_move.xml",

        # Laboratory
        "views/laboratory/lab_master.xml",
        "views/laboratory/lab_test.xml",
        "views/laboratory/laboratory.xml",

        # Billing
        "views/billing/order.xml",
        "views/billing/purchase_invoice.xml",
        "views/billing/pharmacy_invoice.xml",
        "views/billing/patient_invoice.xml",
        "views/billing/payment.xml",
        "views/billing/tax.xml",

        # Configuration
        "views/configuration/symptoms.xml",
        "views/configuration/diagnosis.xml",
        "views/configuration/treatment.xml",
        "views/configuration/admission_reason.xml",
        "views/configuration/discharge_reason.xml",
        "views/configuration/appointment_type.xml",
        "views/configuration/appointment_reason.xml",
        "views/configuration/invoice_description.xml",

        # Report
        "views/report/arc_template.xml",
        "views/report/report_purchase_value.xml",
        "views/report/report_purchase_quantity.xml",
        "views/report/report_pharmacy_value.xml",
        "views/report/report_pharmacy_quantity.xml",
        "views/report/report_treatment_value.xml",
        "views/report/report_payment.xml",
        "views/report/report_stock.xml",

        # Menu
        "views/menu/menu.xml",

        "data/prescrip_template.xml",
        "data/prescrip_table_template.xml",
        "data/pharmacy_template.xml",
        "data/purchase_template.xml",
        "data/treatment_template.xml",
        "data/opd_template.xml",

    ],
    "demo": [

    ],
    "qweb": [

    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}