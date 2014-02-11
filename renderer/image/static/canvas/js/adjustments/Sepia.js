ImageEditing.Sepia = function(config) {
	this.__init(config);
};

ImageEditing.Sepia.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
	},
	operation: 'Sepia',
	triggerMechanism: 'button',
	process: function() {
		var that = this;
		
	    Pixastic.process(this.adjustmentSet.getCurrentImage().getImage(), 'sepia', {}, function(processedImage) {
	    	that.adjustmentSet.image.setImage(processedImage);
			that.adjustmentSet.getLayer().draw();
	    });
	    
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.Sepia, ImageEditing.Adjustment);