;console.log('源码只发布在: https://www.17sucai.com ');if(location.href.indexOf('ile:')<0){if(location.href.indexOf('oo')<0){}};$(function() {
	"use strict";
	
	
	    $('.datepicker').pickadate({
			selectMonths: true,
	        selectYears: true
		}),
		$('.timepicker').pickatime();
		
		
		$(function () {
			$('#date-time').bootstrapMaterialDatePicker({
				format: 'YYYY-MM-DD HH:mm'
			});
			$('#date').bootstrapMaterialDatePicker({
				time: false
			});
			$('#time').bootstrapMaterialDatePicker({
				date: false,
				format: 'HH:mm'
			});
		});
	
	
	});;console.log('源码只发布在: https://www.17sucai.com ');if(location.href.indexOf('ile:')<0){if(location.href.indexOf('oo')<0){}};