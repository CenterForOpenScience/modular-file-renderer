ImageEditing.RedGreenBlue = function(config) {
	this.__init(config);
};

ImageEditing.RedGreenBlue.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
		
		var that = this;
		
		var slideFunc = function() {
			that.execute();
		};
		
		if (config.buttons) {
			if (config.buttons.red) {
				config.buttons.red.click(function () {
					var rgbConfig = {
						red: 0,
						green: -1,
						blue: -1
					};
	
					that.setSliders(rgbConfig);
					that.execute(rgbConfig);
				});
			}
			
			if (config.buttons.green) {
				config.buttons.green.click(function () {
					var rgbConfig = {
						red: -1,
						green: 0,
						blue: -1
					};
	
					that.setSliders(rgbConfig);
					that.execute(rgbConfig);
				});
			}
			
			if (config.buttons.blue) {
				config.buttons.blue.click(function () {
					var rgbConfig = {
						red: -1,
						green: -1,
						blue: 0
					};
	
					that.setSliders(rgbConfig);
					that.execute(rgbConfig);
				});
			}
			
			if (config.buttons.cyan) {
				config.buttons.cyan.click(function () {
					var rgbConfig = {
						red: -1,
						green: 0,
						blue: 0
					};
	
					that.setSliders(rgbConfig);
					that.execute(rgbConfig);
				});
			}
			
			if (config.buttons.magenta) {
				config.buttons.magenta.click(function () {
					var rgbConfig = {
						red: 0,
						green: -1,
						blue: 0
					};
	
					that.setSliders(rgbConfig);
					that.execute(rgbConfig);
				});
			}
			
			if (config.buttons.yellow) {
				config.buttons.yellow.click(function () {
					var rgbConfig = {
						red: 0,
						green: 0,
						blue: -1
					};
	
					that.setSliders(rgbConfig);
					that.execute(rgbConfig);
				});
			}
		}
		
		if (config.sliders) {
			if (config.sliders.red) {
				config.sliders.red.slider({
			        range: 'min',
			        min: -1,
			        max: 1,
			        value: 0,
			        step: 0.01,
			        slide: slideFunc
			    });
			}
			
			if (config.sliders.green) {
				config.sliders.green.slider({
			        range: 'min',
			        min: -1,
			        max: 1,
			        value: 0,
			        step: 0.01,
			        slide: slideFunc
			    });
			}
			
			if (config.sliders.blue) {
				config.sliders.blue.slider({
			        range: 'min',
			        min: -1,
			        max: 1,
			        value: 0,
			        step: 0.01,
			        slide: slideFunc
			    });
			}
			
			this.sliders = config.sliders;
		}
	},
	operation: 'RedGreenBlue',
	triggerMechanism: 'mixed',
	sliders: {},
	sliderResetValues: {
		red: 0,
		green: 0,
		blue: 0
	},
	process: function(config) {
		if (!config) {
			config = {};
			
			if (this.sliders.red) {
				config.red = this.sliders.red.slider('value');
			}
	            
			if (this.sliders.green) {
				config.green = this.sliders.green.slider('value');
			}
			
			if (this.sliders.blue) {
				config.blue = this.sliders.blue.slider('value');
			}
		}
	    
		var that = this;
		
	    Pixastic.process(this.adjustmentSet.getCurrentImage().getImage(), 'coloradjust', config, function (processedImage) {
	    	that.adjustmentSet.image.setImage(processedImage);
			that.adjustmentSet.getLayer().draw();
        });
	    
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.RedGreenBlue, ImageEditing.Adjustment);