ImageEditing.Sharpen = function(config) {
	this.__init(config);
};

ImageEditing.Sharpen.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
		
		var that = this;
		
		var slideFunc = function() {
			that.execute();
		};
		
		if (config.sliders.sharpen) {
			config.sliders.sharpen.slider({
		        min: 0,
		        max: 1,
		        value: 0,
		        step: 0.01,
		        slide: slideFunc
		    });
		}
		
		this.sliders = config.sliders;
	},
	operation: 'Sharpen',
	triggerMechanism: 'slider',
	sliders: {},
	sliderResetValues: {
		sharpen: 0
	},
	process: function() {
		var config = {};
		
		if (this.sliders.sharpen) {
			config.amount = this.sliders.sharpen.slider('value');
		}
	    
		var that = this;
		
	    Pixastic.process(this.adjustmentSet.getCurrentImage().getImage(), 'sharpen', config, function (processedImage) {
	    	that.adjustmentSet.image.setImage(processedImage);
			that.adjustmentSet.getLayer().draw();
        });
	    
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.Sharpen, ImageEditing.Adjustment);