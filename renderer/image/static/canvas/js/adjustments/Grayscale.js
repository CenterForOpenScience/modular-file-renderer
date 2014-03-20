ImageEditing.Grayscale = function(config) {
	this.__init(config);
};

ImageEditing.Grayscale.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
	},
	operation: 'Grayscale',
	triggerMechanism: 'button',
	process: function() {
		var that = this;
		
	    Pixastic.process(this.adjustmentSet.getCurrentImage().getImage(), 'desaturate', {}, function(processedImage) {
	    	that.adjustmentSet.image.setImage(processedImage);
			that.adjustmentSet.getLayer().draw();
	    });
	    
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.Grayscale, ImageEditing.Adjustment);