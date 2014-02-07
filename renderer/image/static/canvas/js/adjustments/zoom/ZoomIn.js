ImageEditing.ZoomIn = function(config) {
	this.___init(config);
};

ImageEditing.ZoomIn.prototype = {
	___init: function(config) {
		ImageEditing.Zoom.call(this, config);
	},
	operation: 'ZoomIn',
	triggerMechanism: 'button',
	process: function() {
	    this.zoom(PointGeometry.scalarToXYVector(1.2));
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.ZoomIn, ImageEditing.Zoom);