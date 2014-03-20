ImageEditing.Edges2 = function(config) {
	this.__init(config);
};

ImageEditing.Edges2.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
	},
	operation: 'Edges2',
	triggerMechanism: 'button',
	process: function() {
		var that = this;
		
	    Pixastic.process(this.adjustmentSet.getCurrentImage().getImage(), 'edges2', {}, function(processedImage) {
	    	that.adjustmentSet.image.setImage(processedImage);
			that.adjustmentSet.getLayer().draw();
	    });
	    
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.Edges2, ImageEditing.Adjustment);