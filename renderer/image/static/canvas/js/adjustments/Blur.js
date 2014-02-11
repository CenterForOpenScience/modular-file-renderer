ImageEditing.Blur = function(config) {
	this.__init(config);
};

ImageEditing.Blur.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
	},
	operation: 'Blur',
	triggerMechanism: 'button',
	process: function() {
		var that = this;
		
	    Pixastic.process(this.adjustmentSet.getCurrentImage().getImage(), 'blur', {}, function(processedImage) {
	    	that.adjustmentSet.image.setImage(processedImage);
			that.adjustmentSet.getLayer().draw();
	    });
	    
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.Blur, ImageEditing.Adjustment);
