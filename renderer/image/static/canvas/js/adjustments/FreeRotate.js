ImageEditing.FreeRotate = function(config) {
	this.__init(config);
};

ImageEditing.FreeRotate.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
	},
	operation: 'FreeRotate',
	triggerMechanism: 'button',
	process: function() {
		if(typeof(this.onStart) === 'function') {
			this.onStart();
		}
		
		var imageLayer = this.adjustmentSet.getLayer();
		var imageGroup = imageLayer.get('.imageGroup')[0];
		var stage = this.adjustmentSet.stage;
		
		var imageGroupOffset = {
			x: stage.getWidth() / 2,
			y: stage.getHeight() / 2
		};
		
		imageGroup.setPosition(imageGroupOffset);
		imageGroup.setOffset(imageGroupOffset);
		
	    var layer = this.layer = new Kinetic.Layer();
	    
	    var group = new Kinetic.Group({
	    	x: stage.getWidth() / 2,
	    	y: stage.getHeight() / 2,
	    	opacity: 0.6
	    });
	    
	    var radius = stage.getWidth() / 4;
	
	    var arc = new Kinetic.Shape({
	        drawFunc: function (context) {
	            context.beginPath();
	            context.arc(0, 0, radius, Math.PI / -10, Math.PI / 10);
	            context.fillStrokeShape(this);
	        },
	        rotation: -Math.PI / 2,
	        stroke: 'yellow',
	        strokeWidth: 6
	    });
	    
	    var circle0 = new Kinetic.Circle({
	        radius: radius,
	        stroke: 'white',
	        strokeWidth: 6
	    });
	
	    var circle1 = new Kinetic.Circle({
	    	radius: radius - 3,
	    	stoke: 'black',
	    	strokeWidth: 1
	    });
	    
	    var circle2 = new Kinetic.Circle({
	    	radius: radius + 3,
	    	stoke: 'black',
	    	strokeWidth: 1
	    });
	
	    var initialRotation = 0;
	    var rotateImage = false;
	    
	    function swapClasses(removingClass, addingClass) {
	    	$(stage.getContainer()).find('canvas').removeClass(removingClass).addClass(addingClass);
	    }
	        
	    layer.on('mousedown', function (e) {
	    	initialRotation = imageGroup.getRotation() - Math.atan2(e.layerY - stage.getHeight() / 2, e.layerX - stage.getWidth() / 2);
	    	arc.setStroke('lawngreen');
	    	rotateImage = true;
	    	swapClasses('grab', 'grabbing');
	    });
	    
	    layer.on('mouseup', function (e) {
	    	arc.setStroke('yellow');
	    	rotateImage = false;
	    	swapClasses('grabbing', 'grab');
	    });
	    
	    // NEED TO ANIMATE THIS
	    layer.on('mousemove', function (e) {
	    	var position = stage.getPointerPosition();
	    	
	    	if (position !== undefined) {
		    	position.x -= stage.getWidth() / 2;
		    	position.y -= stage.getHeight() / 2;
		    	
		        var newRadius = Math.sqrt(Math.pow(position.x, 2) + Math.pow(position.y, 2));
		        
		        if (newRadius > 0) {
		        	var rotation = Math.atan2(position.y, position.x);
	
		            arc.setRotation(rotation);
		            
		        	if (rotateImage) {
		        		imageGroup.setRotation(rotation + initialRotation);
			            imageLayer.draw();
		        	} else {
			            radius = newRadius;
			            circle0.setRadius(newRadius);
			            circle1.setRadius(newRadius - 3);
			            circle2.setRadius(newRadius + 3);
		        	}
		        	
		        	layer.draw();
		        }
	    	}
	    });
	    
	    group.add(circle0);
	    group.add(arc);
	    group.add(circle1);
	    group.add(circle2);
	    
	    layer.add(group);
	    
	    layer.add(new Kinetic.Rect({
	        width: stage.getWidth(),
	        height: stage.getHeight()
	    }));
	    
	    var textBox = new Kinetic.Group({
	    	x: stage.getWidth() / 2,
	    	y: stage.getHeight() / 2
	    });
	    
	    var text = new Kinetic.Text({
	        text: 'Double click to accept.\nDouble right click to cancel.',
	        fontSize: 18,
	        fontFamily: 'Calibri',
	        fill: '#555',
	        width: 250,
	        padding: 20,
	        align: 'center'
	    });
	
		var rect = new Kinetic.Rect({
		    stroke: '#555',
		    strokeWidth: 1,
		    fill: '#ddd',
		    width: 250,
		    height: text.getHeight(),
		    shadowColor: 'black',
		    shadowBlur: 10,
		    shadowOffset: [10, 10],
		    shadowOpacity: 0.2,
		    cornerRadius: 10
		});
		    
		textBox.add(rect);
		textBox.add(text);
		textBox.setOffset(rect.getWidth() / 2, rect.getHeight() / 2);
		 	 
		layer.add(textBox);
		
		var that = this;
		
	    layer.on('dblclick', function (e) {
	    	if (e.button == 2) {
	    		that.cancel();
	    	} else {
	    		that.accept();
	    	}
	    });
		
		stage.add(layer);
		
		// Must only initialize tween after adding the node to the stage.
		var tween = new Kinetic.Tween({
	        node: textBox, 
	        easing: Kinetic.Easings.EaseIn,
	        duration: 3,
	        opacity: 0,
	        onFinish: function() {
	        	textBox.destroyChildren();
	        	textBox.destroy();
	        }
	    });
		
		tween.play();
		
		$(stage.getContainer()).find('canvas').addClass('grab');
	},
	reset: function() {
		this.layer.destroyChildren();
	    this.layer.destroy();
	    $(this.adjustmentSet.stage.getContainer()).find('canvas').removeClass('grab');
	    this.adjustmentSet.stage.draw();
	    
	    if(typeof(this.onFinish) === 'function') {
	    	this.onFinish();
	    }
	},
	cancel: function() {
		this.adjustmentSet.getLayer().get('.imageGroup')[0].setRotation(0);
		this.reset();
	},
	accept: function() {
		var imageLayer = this.adjustmentSet.getLayer(),
			imageGroup = imageLayer.get('.imageGroup')[0],
			image = imageGroup.get('.image')[0],
			landmarks = imageGroup.get('.landmarks')[0];
			
		image.absoluteRotation += imageGroup.getRotation();
			
		var rotatedSize = getRotatedSize(image.originalSize, image.absoluteRotation);
			
		Pixastic.process(image.getImage(), 'rotate', {
			angle: imageGroup.getRotation()
		},
		function(processedImage) {
			// NEED TO WORK ON CROPPING FUNCTION, CAN SET IMAGE TO CANVAS
			Pixastic.process(processedImage, 'crop', {
				rect: {
					top: Math.ceil((processedImage.height - rotatedSize.height) / 2),
					left: Math.ceil((processedImage.width - rotatedSize.width) / 2),
					width: rotatedSize.width,
					height: rotatedSize.height
				}
			},
			function(processedImage) {
				image.setPosition(toRotatedGroupSpace(imageGroup.getPosition(), image.getPosition(), imageGroup.getRotation()));
				image.setImage(processedImage);
				image.setOffset({
					x: processedImage.width / 2,
					y: processedImage.height / 2
				});
				
				if (landmarks) {
					landmarks.setRotation(image.absoluteRotation);
					landmarks.setPosition(image.getPosition());
				}
				
				imageGroup.setRotation(0);
				imageLayer.draw();
			});
		});
		
		this.complete();
		this.reset();   
	}
};

Kinetic.Util.extend(ImageEditing.FreeRotate, ImageEditing.Adjustment);