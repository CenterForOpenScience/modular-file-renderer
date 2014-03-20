ImageEditing.Fit = function(config) {
	this.__init(config);
};

ImageEditing.Fit.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
	},
	getBannerHeight: function() {
		var bannersLayer = this.adjustmentSet.stage.get('.classificationBanner')[0];
		
		if (bannersLayer) {
			var banner = bannersLayer.getChildren()[0];
			
			if (banner) {
				return banner.getHeight();		
			}
		}
		
		return 0;
	}
};

Kinetic.Util.extend(ImageEditing.Fit, ImageEditing.Adjustment);