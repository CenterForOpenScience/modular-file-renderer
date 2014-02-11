ImageEditing.Undo = function(config) {
	this.__init(config);
};

ImageEditing.Undo.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
		
		var that = this;
	
		this.execute = function() {
			if (that.adjustmentSet.lastOperation != that.operation && that.adjustmentSet.lastOperation != 'Redo')
				that.adjustmentSet.updateImages();
			
			that.process();
		};
		
		config.button.click(that.execute);
	},
	operation: 'Undo',
	triggerMechanism: 'special',
	process: function() {
        if (this.adjustmentSet.currentImage < this.adjustmentSet.imagesCache.length - 2) {
        	this.adjustmentSet.image.destroy();
            this.adjustmentSet.image = this.adjustmentSet.cloneImage(this.adjustmentSet.imagesCache[++(this.adjustmentSet.currentImage)]);
            this.adjustmentSet.getLayer().get('.imageGroup')[0].add(this.adjustmentSet.image);
    		if (this.adjustmentSet.landmarks) this.adjustmentSet.landmarks.updateLandmarks();
            this.adjustmentSet.getLayer().draw();
        } else {
            alert('Cannot Undo Further');
        }
        
		this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.Undo, ImageEditing.Adjustment);