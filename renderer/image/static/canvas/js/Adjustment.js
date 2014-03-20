ImageEditing.Adjustment = function(config) {
	var that = this;

    if (config.onStart) this.onStart = config.onStart;
    if (config.onFinish) this.onFinish = config.onFinish;

	this.execute = function(config) {
		if (that.triggerMechanism == 'button' || that.adjustmentSet.lastOperation != that.operation)
			that.adjustmentSet.updateImages();
		
		that.process(config);
	};
	
	this.complete = function() {
		that.adjustmentSet.resetAllSlidersExcept(that.operation);
		that.adjustmentSet.setLastOperation(that.operation);
	};
	
	if (this.triggerMechanism == 'button') {
		config.button.click(that.execute);
	}
};

ImageEditing.Adjustment.prototype = {
	setSliders: function(values) {
		for (var i in this.sliders) {
			this.sliders[i].slider('value', values[i]);
		}
	}
};
