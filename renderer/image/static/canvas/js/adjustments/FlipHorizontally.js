ImageEditing.FlipHorizontally = function(config) {
	this.__init(config);
};

ImageEditing.FlipHorizontally.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
	},
	operation: 'FlipHorizontally',
	triggerMechanism: 'button',
	process: function() {
		var that = this;
		
		Pixastic.process(this.adjustmentSet.getCurrentImage().getImage(), 'fliph', {}, function(processedImage) {
	    	that.adjustmentSet.image.setImage(processedImage);
	    	that.adjustmentSet.image.setX(that.adjustmentSet.getLayer().get('.imageGroup')[0].getX() * 2 - that.adjustmentSet.image.getX());
	    	that.adjustmentSet.image.isFlippedHorizontally = !that.adjustmentSet.image.isFlippedHorizontally;
			if (that.adjustmentSet.landmarks) that.adjustmentSet.landmarks.updateLandmarks();
			that.adjustmentSet.getLayer().draw();
		});
		
		this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.FlipHorizontally, ImageEditing.Adjustment);