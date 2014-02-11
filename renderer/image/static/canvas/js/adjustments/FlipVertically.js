ImageEditing.FlipVertically = function(config) {
	this.__init(config);
};

ImageEditing.FlipVertically.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
	},
	operation: 'FlipVertically',
	triggerMechanism: 'button',
	process: function() {
		var that = this;
		
	    Pixastic.process(this.adjustmentSet.getCurrentImage().getImage(), 'flipv', {}, function(processedImage) {
	    	that.adjustmentSet.image.setImage(processedImage);
	    	that.adjustmentSet.image.setY(that.adjustmentSet.getLayer().get('.imageGroup')[0].getY() * 2 - that.adjustmentSet.image.getY());
	    	that.adjustmentSet.image.isFlippedVertically = !that.adjustmentSet.image.isFlippedVertically;
			if (that.adjustmentSet.landmarks) that.adjustmentSet.landmarks.updateLandmarks();
			that.adjustmentSet.getLayer().draw();
	    });
	    
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.FlipVertically, ImageEditing.Adjustment);