ImageEditing.Edges = function(config) {
	this.__init(config);
};

ImageEditing.Edges.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
	},
	operation: 'Edges',
	triggerMechanism: 'button',
	process: function() {
		var that = this;
		
	    Pixastic.process(this.adjustmentSet.getCurrentImage().getImage(), 'edges', {}, function(processedImage) {
	    	that.adjustmentSet.image.setImage(processedImage);
			that.adjustmentSet.getLayer().draw();
	    });
	    
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.Edges, ImageEditing.Adjustment);