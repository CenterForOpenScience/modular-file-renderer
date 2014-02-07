ImageEditing.ZoomOriginal = function(config) {
	this.___init(config);
};

ImageEditing.ZoomOriginal.prototype = {
	___init: function(config) {
		ImageEditing.Zoom.call(this, config);
	},
	operation: 'ZoomOriginal',
	triggerMechanism: 'button',
	process: function() {
	    this.zoom(PointGeometry.divide(PointGeometry.scalarToXYVector(1), this.adjustmentSet.image.getScale()));
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.ZoomOriginal, ImageEditing.Zoom);