ImageEditing.HueSaturationLightness = function(config) {
	this.__init(config);
};

ImageEditing.HueSaturationLightness.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
		
		var that = this;
		
		var slideFunc = function() {
			that.execute();
		};
		
		if (config.sliders.hue) {
			config.sliders.hue.slider({
		    	min: -180,
		        max: 180,
		        value: 0,
		        step: 1,
		        slide: slideFunc
		    });
		}
		
		if (config.sliders.saturation) {
			config.sliders.saturation.slider({
		        min: -100,
		        max: 100,
		        value: 0,
		        step: 1,
		        slide: slideFunc
		    });
		}
		
		if (config.sliders.lightness) {
			config.sliders.lightness.slider({
		        min: -100,
		        max: 100,
		        value: 0,
		        step: 1,
		        slide: slideFunc
		    });
		}
		
		this.sliders = config.sliders;
	},
	operation: 'HueSaturationLightness',
	triggerMechanism: 'slider',
	sliders: {},
	sliderResetValues: {
		hue: 0,
		saturation: 0,
		lightness: 0
	},
	process: function() {
		var config = {};
		
		if (this.sliders.hue) {
			config.hue = this.sliders.hue.slider('value');
		}
            
        if (this.sliders.contrast) {
        	config.contrast = this.sliders.contrast.slider('value');
        }
	    
	    if (this.sliders.lightness) {
	    	config.lightness = this.sliders.lightness.slider('value');
	    }
	    
		var that = this;
		
	    Pixastic.process(this.adjustmentSet.getCurrentImage().getImage(), 'hsl', config, function (processedImage) {
	    	that.adjustmentSet.image.setImage(processedImage);
			that.adjustmentSet.getLayer().draw();
        });
	    
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.HueSaturationLightness, ImageEditing.Adjustment);