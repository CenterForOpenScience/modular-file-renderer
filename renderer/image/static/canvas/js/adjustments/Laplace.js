ImageEditing.Laplace = function(config) {
	this.__init(config);
};

ImageEditing.Laplace.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
	},
	operation: 'Laplace',
	triggerMechanism: 'button',
	process: function() {
		var that = this;
	 
	    Pixastic.process(this.adjustmentSet.getCurrentImage().getImage(), 'laplace', { edgeStrength: 5.0 }, function(processedImage) {
	    	that.adjustmentSet.image.setImage(processedImage);
			that.adjustmentSet.getLayer().draw();
	    });
	    
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.Laplace, ImageEditing.Adjustment);