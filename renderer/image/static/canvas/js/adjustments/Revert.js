ImageEditing.Revert = function(config) {
	this.__init(config);
};

ImageEditing.Revert.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
	},
	operation: 'Revert',
	triggerMechanism: 'button',
	process: function() {
        this.adjustmentSet.image.destroy();
        this.adjustmentSet.image = this.adjustmentSet.cloneImage(this.adjustmentSet.firstImage);
        this.adjustmentSet.getLayer().get('.imageGroup')[0].add(this.adjustmentSet.image);
        if (this.adjustmentSet.landmarks) this.adjustmentSet.landmarks.updateLandmarks();
        this.adjustmentSet.getLayer().draw();    
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.Revert, ImageEditing.Adjustment);