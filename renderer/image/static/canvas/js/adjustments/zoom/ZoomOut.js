ImageEditing.ZoomOut = function(config) {
	this.___init(config);
};

ImageEditing.ZoomOut.prototype = {
	___init: function(config) {
		this.operation = 'ZoomOut';
		this.triggerMechanism = 'button';
		
		ImageEditing.Zoom.call(this, config);
		
		this.process = function() {
		    this.zoom(PointGeometry.scalarToXYVector(1.0 / 1.2));
		};
	},
};

Kinetic.Util.extend(ImageEditing.ZoomOut, ImageEditing.Zoom);