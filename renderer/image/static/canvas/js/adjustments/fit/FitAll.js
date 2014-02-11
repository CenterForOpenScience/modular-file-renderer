ImageEditing.FitAll = function(config) {
	this.___init(config);
};

ImageEditing.FitAll.prototype = {
	___init: function(config) {
		ImageEditing.Fit.call(this, config);
	},
	operation: 'FitAll',
	triggerMechanism: 'button',
	process: function() {
	    var stageSize = this.adjustmentSet.stage.getSize(),
    		imageSize = this.adjustmentSet.image.getSize(),
			bannersHeight = this.getBannerHeight() * 2,
        	scaleHeight = (stageSize.height - bannersHeight) / imageSize.height,
        	scaleWidth = stageSize.width / imageSize.width;
        	
	    this.adjustmentSet.image.setScale(PointGeometry.scalarToXYVector(scaleWidth < scaleHeight ? scaleWidth : scaleHeight));
    	this.adjustmentSet.image.setPosition(stageSize.width / 2, stageSize.height / 2);
    	if (this.adjustmentSet.landmarks) this.adjustmentSet.landmarks.updateLandmarks();
		this.adjustmentSet.getLayer().draw();
		this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.FitAll, ImageEditing.Fit);