frappe.ui.form.on('Quotation', {
    markup_option: function(frm) {
	if(parseInt(frm.doc.markup_option) > 0){
		$.each(frm.doc.items || [], function(i, v) {
			console.log(v.rate)
			var rate = v.rate;
			frappe.model.set_value(v.doctype, v.name, "rate", ((parseInt(frm.doc.markup_option) * parseInt(rate))/100)+ rate )
		})
		}
	}
})