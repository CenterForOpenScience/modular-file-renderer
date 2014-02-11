ImageEditing.Zoom = function(config) {
	this.__init(config);
};

ImageEditing.Zoom.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
	},
	zoom: function(zoomFactor) {
        this.adjustmentSet.image.move(
        	PointGeometry.multiply(
        		PointGeometry.subtract({
			    	x: this.adjustmentSet.stage.getWidth() / 2,
			    	y: this.adjustmentSet.stage.getHeight() / 2
	    		},
	    		this.adjustmentSet.image.getPosition()),
        		PointGeometry.subtract(PointGeometry.scalarToXYVector(1), zoomFactor)
        	)
        );
        
        this.adjustmentSet.image.setScale(PointGeometry.multiply(this.adjustmentSet.image.getScale(), zoomFactor));
        if (this.adjustmentSet.landmarks) this.adjustmentSet.landmarks.updateLandmarks();
        this.adjustmentSet.getLayer().draw();
	}
};

Kinetic.Util.extend(ImageEditing.Zoom, ImageEditing.Adjustment);