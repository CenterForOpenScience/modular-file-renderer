ImageEditing.FitHeight = function(config) {
	this.___init(config);
};

ImageEditing.FitHeight.prototype = {
	___init: function(config) {
		ImageEditing.Fit.call(this, config);
	},
	operation: 'FitHeight',
	triggerMechanism: 'button',
	process: function() {
	    var stageSize = this.adjustmentSet.stage.getSize(),
    		imageSize = this.adjustmentSet.image.getSize(),
			bannersHeight = this.getBannerHeight() * 2;
        	
	    this.adjustmentSet.image.setScale(PointGeometry.scalarToXYVector((stageSize.height - bannersHeight) / imageSize.height));
    	this.adjustmentSet.image.setPosition(stageSize.width / 2, stageSize.height / 2);
    	if (this.adjustmentSet.landmarks) this.adjustmentSet.landmarks.updateLandmarks();
    	this.adjustmentSet.getLayer().draw();
		this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.FitHeight, ImageEditing.Fit);