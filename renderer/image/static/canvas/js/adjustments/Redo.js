ImageEditing.Redo = function(config) {
	this.__init(config);
};

ImageEditing.Redo.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
		
		var that = this;
		
		this.execute = function() {
			that.process();
		};
		
		config.button.click(that.execute);
	},
	operation: 'Redo',
	triggerMechanism: 'special',
	process: function() {
        if (this.adjustmentSet.currentImage > 0) {
        	this.adjustmentSet.image.destroy();
            this.adjustmentSet.image = this.adjustmentSet.cloneImage(this.adjustmentSet.imagesCache[--this.adjustmentSet.currentImage]);
			this.adjustmentSet.getLayer().get('.imageGroup')[0].add(this.adjustmentSet.image);
    		if (this.adjustmentSet.landmarks) this.adjustmentSet.landmarks.updateLandmarks();
            this.adjustmentSet.getLayer().draw();
        } else {
            alert('Cannot Redo Further');
        }
	    
	    this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.Redo, ImageEditing.Adjustment);