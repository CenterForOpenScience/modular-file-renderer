ImageEditing.AdjustmentSet = function(config) {
	this.cloneImage = function(image) {
		var newImage = image.clone();
		
		newImage.absoluteRotation = image.absoluteRotation;
		newImage.isFlippedVertically = image.isFlippedVertically;
		newImage.isFlippedHorizontally = image.isFlippedHorizontally;
		newImage.originalSize = image.originalSize;
		
		return newImage;
	};

	this.image = config.layer.get('.image')[0];
    this.landmarks = config.layer.get('.landmarks')[0];
    this.stage = config.layer.getStage();
    this.firstImage = this.cloneImage(this.image);
    
	this.imagesCache = [this.cloneImage(this.image)];
    
    this.getCurrentImage = function() {
    	return this.imagesCache[0];
    };
    
    this.lastOperation = null;
    this.currentImage = 0;

	this.updateImages = function() {
        if (this.imagesCache.unshift(this.cloneImage(this.image)) > 10) {
            this.imagesCache.pop();
        }

        this.currentImage = 0;
   	};
    
    this.setLastOperation = function(operation) {
    	this.lastOperation = operation;
    };
    
    var adjustments = [];
    
    var that = this;
    
    this.getLayer = function() {
    	return config.layer;
    };
    
    this.resetAllSlidersExcept = function (operation) {
        for (var i = 0; i < adjustments.length; i++) {
        	if (operation != adjustments[i].operation) {
        		adjustments[i].setSliders(adjustments[i].sliderResetValues);
        	}
        }
    };
    
    this.add = function(adjustment) {
    	adjustment.adjustmentSet = that;
	    adjustments.push(adjustment);
    };
};