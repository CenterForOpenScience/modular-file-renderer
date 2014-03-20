ImageEditing.Pan = function(config) {
	this.__init(config);
};

ImageEditing.Pan.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
	},
	operation: 'Pan',
	triggerMechanism: 'button',
	process: function() {
		var that = this;
		
        this.adjustmentSet.image.setDraggable(true);
        $(this.adjustmentSet.getLayer().getStage().getContainer()).find('canvas').addClass('grab');
        
        this.adjustmentSet.image.on('dragstart', function() {
        	$(that.adjustmentSet.getLayer().getStage().getContainer()).find('canvas').removeClass('grab').addClass('grabbing');
        	if (that.adjustmentSet.landmarks) that.adjustmentSet.landmarks.animPos.start();
        });
        
        this.adjustmentSet.image.on('dragend', function () {
        	$(that.adjustmentSet.getLayer().getStage().getContainer()).find('canvas').removeClass('grabbing');
            that.adjustmentSet.image.setDraggable(false);
            if (that.adjustmentSet.landmarks) {
	            that.adjustmentSet.landmarks.animPos.stop();
	            that.adjustmentSet.landmarks.updateLandmarks();
            }
            that.complete();
        });
	}
};

Kinetic.Util.extend(ImageEditing.Pan, ImageEditing.Adjustment);