ImageEditing.FitWidth = function(config) {
	this.___init(config);
};

ImageEditing.FitWidth.prototype = {
	___init: function(config) {
		ImageEditing.Fit.call(this, config);
	},
	operation: 'FitWidth',
	triggerMechanism: 'button',
	process: function() {
	    var stageSize = this.adjustmentSet.stage.getSize(),
    		imageSize = this.adjustmentSet.image.getSize();
        	
	    this.adjustmentSet.image.setScale(PointGeometry.scalarToXYVector(stageSize.width / imageSize.width));
    	this.adjustmentSet.image.setPosition(stageSize.width / 2, stageSize.height / 2);
    	if (this.adjustmentSet.landmarks) this.adjustmentSet.landmarks.updateLandmarks();
		this.adjustmentSet.getLayer().draw();
		this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.FitWidth, ImageEditing.Fit);