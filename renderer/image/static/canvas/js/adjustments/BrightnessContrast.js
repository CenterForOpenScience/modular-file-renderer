ImageEditing.BrightnessContrast = function(config) {
	this.__init(config);
};

ImageEditing.BrightnessContrast.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
		
		var that = this;
		
		var slideFunc = function() {
			that.execute();
		};
		
		if (config.sliders.brightness) {
			config.sliders.brightness.slider({
		        min: -150,
		        max: 150,
		        value: 0,
		        step: 1,
		        slide: slideFunc
		    });
		}
		
		if (config.sliders.contrast) {
			config.sliders.contrast.slider({
		        min: -5,
		        max: 5,
		        value: 0,
		        step: 0.1,
		        slide: slideFunc
		    });
		}
		
		this.sliders = config.sliders;
	},
	operation: 'BrightnessContrast',
	triggerMechanism: 'slider',
	sliders: {},
	sliderResetValues: {
		brightness: 0,
		contrast: 0
	},
	process: function() {
		var config = {};
		
		if (this.sliders.brightness) {
			config.brightness = this.sliders.brightness.slider('value');
		}
            
        if (this.sliders.contrast) {
        	config.contrast = this.sliders.contrast.slider('value') < 0 ? this.sliders.contrast.slider('value') / 5 : this.sliders.contrast.slider('value');
        }
	    
		var that = this;
		
	    Pixastic.process(this.adjustmentSet.getCurrentImage().getImage(), 'brightness', config, function (processedImage) {
	    	that.adjustmentSet.image.setImage(processedImage);
			that.adjustmentSet.getLayer().draw();
        });
	    
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.BrightnessContrast, ImageEditing.Adjustment);