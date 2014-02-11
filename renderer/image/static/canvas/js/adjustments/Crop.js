// NOT WORKING YET. NEED TO FIGURE OUT CALL STACK EXCEEDED ERROR AND THEN APPLY CROPPING BASED ON BOX BOUNDS.

ImageEditing.Crop = function(config) {
	this.__init(config);
};

ImageEditing.Crop.prototype = {
	__init: function(config) {
		ImageEditing.Adjustment.call(this, config);
	},
	operation: 'Crop',
	triggerMechanism: 'button',
	process: function() {
		if(typeof(this.onStart) === 'function') {
			this.onStart();
		}

		var that = this;


		function getBounds(node, useAbsolutePosition) {
	        var position = useAbsolutePosition ? node.getAbsolutePosition() : node.getPosition(),
	            offset = node.getOffset(),
	            size = node.getSize(),
	            scale = node.getScale();
	
	        var x1 = position.x - offset.x * scale.x,
	            xLength = size.width * scale.x,
	            x2 = x1 + xLength,
	            x1LTx2 = x1 < x2,
	            y1 = position.y - offset.y * scale.y,
	            yLength = size.height * scale.y,
	            y2 = y1 + yLength,
	            y1LTy2 = y1 < y2;
	
	        return {
	            x: {
	                min: x1LTx2 ? x1 : x2,
	                max: x1LTx2 ? x2 : x1,
	                length: Math.abs(xLength),
	                scale: scale.x
	            },
	            y: {
	                min: y1LTy2 ? y1 : y2,
	                max: y1LTy2 ? y2 : y1,
	                length: Math.abs(yLength),
	                scale: scale.y
	            }
	        };
	    }
	
	    function setBounds(left, right, top, bottom) {
	        return {
	            x: {
	                min: left,
	                max: right,
	                length: right - left
	            },
	            y: {
	                min: top,
	                max: bottom,
	                length: bottom - top
	            }
	        };
	    }
	        
	    function getBoundsFromLines(layer) {
	        return setBounds(layer.get('.boxLeftLine')[0].getX(), layer.get('.boxRightLine')[0].getX(), layer.get('.boxTopLine')[0].getY(), layer.get('.boxBottomLine')[0].getY());
	    }
	    
	    function getBoundsFromCorner(layer, cornerName) {
	    	if (cornerName == 'boxTopLeftCorner' || cornerName == 'boxBottomRightCorner') {
	        	var topLeftCorner = layer.get('.boxTopLeftCorner')[0],
	            	bottomRightCorner = layer.get('.boxBottomRightCorner')[0];
	        	
	        	return setBounds(topLeftCorner.getX(), bottomRightCorner.getX(), topLeftCorner.getY(), bottomRightCorner.getY());
	        } else {
	        	var topRightCorner = layer.get('.boxTopRightCorner')[0],
	            	bottomLeftCorner = layer.get('.boxBottomLeftCorner')[0];
	        	
	        	return setBounds(bottomLeftCorner.getX(), topRightCorner.getX(), topRightCorner.getY(), bottomLeftCorner.getY());
	        }
	    }
	    
	    function setLinesAndCorners(layer, boxBounds) {
	    	var topLine = layer.get('.boxTopLine')[0],
		        leftLine = layer.get('.boxLeftLine')[0],
		        rightLine = layer.get('.boxRightLine')[0],
		        bottomLine = layer.get('.boxBottomLine')[0],
		        topLeftCorner = layer.get('.boxTopLeftCorner')[0],
		        topRightCorner = layer.get('.boxTopRightCorner')[0],
		        bottomLeftCorner = layer.get('.boxBottomLeftCorner')[0],
		        bottomRightCorner = layer.get('.boxBottomRightCorner')[0];
	    	
	    	topLine.setPosition(boxBounds.x.min, boxBounds.y.min);
	        bottomLine.setPosition(boxBounds.x.min, boxBounds.y.max);
	        leftLine.setPosition(boxBounds.x.min, boxBounds.y.min);
	        rightLine.setPosition(boxBounds.x.max, boxBounds.y.min);
	
	        leftLine.setPoints([0, 0, 0, boxBounds.y.length]);
	        rightLine.setPoints([0, 0, 0, boxBounds.y.length]);
	        topLine.setPoints([0, 0, boxBounds.x.length, 0]);
	        bottomLine.setPoints([0, 0, boxBounds.x.length, 0]);
	
	        topLeftCorner.setPosition(boxBounds.x.min, boxBounds.y.min);
	        topRightCorner.setPosition(boxBounds.x.max, boxBounds.y.min);
	        bottomLeftCorner.setPosition(boxBounds.x.min, boxBounds.y.max);
	        bottomRightCorner.setPosition(boxBounds.x.max, boxBounds.y.max);
	    }
	
	    function boxWindowImageAdjust(box, img, img2) {
	        var boxBounds = getBounds(box, true),
	            imgBounds = getBounds(img, false),
	            cropWidth,
	            cropHeight;
			
	        if (imgBounds.x.min >= boxBounds.x.max || imgBounds.y.min >= boxBounds.y.max ||
	            imgBounds.x.max <= boxBounds.x.min || imgBounds.y.max <= boxBounds.y.min) {
	            img2.setVisible(false);
	        } else {
	            img2.setVisible(true);
	
	            if (boxBounds.x.max > imgBounds.x.max) {
	                cropWidth = (boxBounds.x.min < imgBounds.x.min ? imgBounds.x.length : imgBounds.x.max - boxBounds.x.min) / imgBounds.x.scale;
	            } else {
	                cropWidth = (boxBounds.x.length + (boxBounds.x.min > imgBounds.x.min ? 0 : boxBounds.x.min - imgBounds.x.min)) / imgBounds.x.scale;
	            }
	
	            if (boxBounds.y.max > imgBounds.y.max) {
	                cropHeight = (boxBounds.y.min < imgBounds.y.min ? imgBounds.y.length : imgBounds.y.max - boxBounds.y.min) / imgBounds.y.scale;
	            } else {
	                cropHeight = (boxBounds.y.length + (boxBounds.y.min > imgBounds.y.min ? 0 : boxBounds.y.min - imgBounds.y.min)) / imgBounds.y.scale;
	            }
	
	            img2.setAbsolutePosition({
	                x: boxBounds.x.min < imgBounds.x.min ? imgBounds.x.min : boxBounds.x.min,
	                y: boxBounds.y.min < imgBounds.y.min ? imgBounds.y.min : boxBounds.y.min
	            });
	            img2.setSize({
	                width: cropWidth,
	                height: cropHeight
	            });
	            img2.setCrop({
	                x: boxBounds.x.min < imgBounds.x.min ? 0 : (boxBounds.x.min - imgBounds.x.min) / Math.abs(imgBounds.x.scale),
	                y: boxBounds.y.min < imgBounds.y.min ? 0 : (boxBounds.y.min - imgBounds.y.min) / Math.abs(imgBounds.y.scale),
	                width: cropWidth,
	                height: cropHeight
	            });
	        }
	    }
	
	    function createBoxWindow(stage, img) {
	        var layer = new Kinetic.Layer({
	            //draggable: true
	        });
	
	        var cornerLength = 10;
	        var strokeWidth = 10;
	
	        var box = new Kinetic.Rect({
	            name: 'windowRect',
	            x: stage.getWidth() / 4,
	            y: stage.getHeight() / 4,
	            width: stage.getWidth() / 2,
	            height: stage.getHeight() / 2,
	            stroke: 'red',
	            strokeWidth: 1,
	            draggable: true,
	            dragBoundFunc: function(pos) {
	            	if (pos.x < 0) pos.x = 0;
	            	if (pos.x > stage.getWidth() - this.getWidth()) pos.x = stage.getWidth() - this.getWidth();
	            	if (pos.y < 0) pos.y = 0;
	            	if (pos.y > stage.getHeight() - this.getHeight()) pos.y = stage.getHeight() - this.getHeight();
	            	
		            return pos;
	            }
	        });
	        
	        function getCanvases() {
		        return $(stage.getContainer()).find('canvas');
	        }
	        
	        box.on('mouseenter', function () {
	            getCanvases().addClass('move');
	        });
	
	        box.on('mouseleave', function () {
	            getCanvases().removeClass('move');
	        });
	
	        layer.add(box);
	
	        var boxBoundsInit = getBounds(box);
	
	        var lineConfigs = [{
	            name: 'boxTopLine',
	            x: boxBoundsInit.x.min,
	            y: boxBoundsInit.y.min,
	            points: [0, 0, box.getWidth(), 0],
	            dragBoundFunc: function (pos, evt) {
	                var yMax = layer.get('.boxBottomLine')[0].getAbsolutePosition().y - strokeWidth;
	
	                return {
	                    x: this.getAbsolutePosition().x,
	                    y: pos.y < yMax ? pos.y : yMax
	                };
	            },
	            onMouseEnterFunc: function () {
	                getCanvases().addClass('ns-resize');
	            },
	            onMouseLeaveFunc: function () {
		            getCanvases().removeClass('ns-resize');
	            }
	        }, {
	            name: 'boxBottomLine',
	            x: boxBoundsInit.x.min,
	            y: boxBoundsInit.y.max,
	            points: [0, 0, box.getWidth(), 0],
	            dragBoundFunc: function (pos, evt) {
	                var yMin = layer.get('.boxTopLine')[0].getAbsolutePosition().y + strokeWidth;
	
	                return {
	                    x: this.getAbsolutePosition().x,
	                    y: pos.y > yMin ? pos.y : yMin
	                };
	            },
	            onMouseEnterFunc: function () {
	                getCanvases().addClass('ns-resize');
	            },
	            onMouseLeaveFunc: function () {
		            getCanvases().removeClass('ns-resize');
	            }
	        }, {
	            name: 'boxLeftLine',
	            x: boxBoundsInit.x.min,
	            y: boxBoundsInit.y.min,
	            points: [0, 0, 0, box.getHeight()],
	            dragBoundFunc: function (pos, evt) {
	                var xMax = layer.get('.boxRightLine')[0].getAbsolutePosition().x - strokeWidth;
	
	                return {
	                    x: pos.x < xMax ? pos.x : xMax,
	                    y: this.getAbsolutePosition().y
	                };
	            },
	            onMouseEnterFunc: function () {
	                getCanvases().addClass('ew-resize');
	            },
	            onMouseLeaveFunc: function () {
		            getCanvases().removeClass('ew-resize');
	            }
	        }, {
	            name: 'boxRightLine',
	            x: boxBoundsInit.x.max,
	            y: boxBoundsInit.y.min,
	            points: [0, 0, 0, box.getHeight()],
	            dragBoundFunc: function (pos, evt) {
	                var xMin = layer.get('.boxLeftLine')[0].getAbsolutePosition().x + strokeWidth;
	
	                return {
	                    x: pos.x > xMin ? pos.x : xMin,
	                    y: this.getAbsolutePosition().y
	                };
	            },
	            onMouseEnterFunc: function () {
	                getCanvases().addClass('ew-resize');
	            },
	            onMouseLeaveFunc: function () {
		            getCanvases().removeClass('ew-resize');
	            }
	        }];
	
	        for (var i = 0, line; i < lineConfigs.length; i++) {
	        	lineConfigs[i].draggable = true;
	        	lineConfigs[i].stroke = 'transparent';
	        	lineConfigs[i].strokeWidth = strokeWidth;
	        	
	            line = new Kinetic.Line(lineConfigs[i]);
	
	            line.on('mouseenter', lineConfigs[i].onMouseEnterFunc);
	            line.on('mouseleave', lineConfigs[i].onMouseLeaveFunc);
	
	            line.on('dragmove', function () {
	                var boxBounds = getBoundsFromLines(layer);
	
	                box.setPosition(boxBounds.x.min, boxBounds.y.min);
	                box.setSize(boxBounds.x.length, boxBounds.y.length);
	            });
	
	            line.on('dragend', function () {
	                //--- This can be done on drag end since they're transparent ---//
	                setLinesAndCorners(layer, getBoundsFromLines(layer));
	                layer.draw();
	            });
	
	            layer.add(line);
	        }
	
	        var cornerConfigs = [{
	            name: 'boxTopLeftCorner',
	            x: boxBoundsInit.x.min,
	            y: boxBoundsInit.y.min,
	            points: [0, cornerLength, 0, 0, cornerLength, 0],
	            dragBoundFunc: function (pos, evt) {
	                var bounds = layer.get('.boxBottomRightCorner')[0].getAbsolutePosition();
	                bounds = {
	                    x: bounds.x - strokeWidth,
	                    y: bounds.y - strokeWidth
	                };
	
	                return {
	                    x: pos.x < bounds.x ? pos.x : bounds.x,
	                    y: pos.y < bounds.y ? pos.y : bounds.y
	                };
	            },
	            onMouseEnterFunc: function () {
	                getCanvases().addClass('nwse-resize');
	            },
	            onMouseLeaveFunc: function () {
		            getCanvases().removeClass('nwse-resize');
	            }
	        }, {
	            name: 'boxTopRightCorner',
	            x: boxBoundsInit.x.max,
	            y: boxBoundsInit.y.min,
	            points: [-cornerLength, 0, 0, 0, 0, cornerLength],
	            dragBoundFunc: function (pos, evt) {
	                var bounds = layer.get('.boxBottomLeftCorner')[0].getAbsolutePosition();
	                bounds = {
	                    x: bounds.x + strokeWidth,
	                    y: bounds.y - strokeWidth
	                };
	
	                return {
	                    x: pos.x > bounds.x ? pos.x : bounds.x,
	                    y: pos.y < bounds.y ? pos.y : bounds.y
	                };
	            },
	            onMouseEnterFunc: function () {
	                getCanvases().addClass('nesw-resize');
	            },
	            onMouseLeaveFunc: function () {
		            getCanvases().removeClass('nesw-resize');
	            }
	        }, {
	            name: 'boxBottomLeftCorner',
	            x: boxBoundsInit.x.min,
	            y: boxBoundsInit.y.max,
	            points: [0, -cornerLength, 0, 0, cornerLength, 0],
	            dragBoundFunc: function (pos, evt) {
	                var bounds = layer.get('.boxTopRightCorner')[0].getAbsolutePosition();
	                bounds = {
	                    x: bounds.x - strokeWidth,
	                    y: bounds.y + strokeWidth
	                };
	
	                return {
	                    x: pos.x < bounds.x ? pos.x : bounds.x,
	                    y: pos.y > bounds.y ? pos.y : bounds.y
	                };
	            },
	            onMouseEnterFunc: function () {
	                getCanvases().addClass('nesw-resize');
	            },
	            onMouseLeaveFunc: function () {
		            getCanvases().removeClass('nesw-resize');
	            }
	        }, {
	            name: 'boxBottomRightCorner',
	            x: boxBoundsInit.x.max,
	            y: boxBoundsInit.y.max,
	            points: [-cornerLength, 0, 0, 0, 0, -cornerLength],
	            dragBoundFunc: function (pos, evt) {
	                var bounds = layer.get('.boxTopLeftCorner')[0].getAbsolutePosition();
	                bounds = {
	                    x: bounds.x + strokeWidth,
	                    y: bounds.y + strokeWidth
	                };
	
	                return {
	                    x: pos.x > bounds.x ? pos.x : bounds.x,
	                    y: pos.y > bounds.y ? pos.y : bounds.y
	                };
	            },
	            onMouseEnterFunc: function () {
	                getCanvases().addClass('nwse-resize');
	            },
	            onMouseLeaveFunc: function () {
		            getCanvases().removeClass('nwse-resize');
	            }
	        }];
	
	        for (var i = 0, corner; i < cornerConfigs.length; i++) {
	        	cornerConfigs[i].draggable = true;
	        	cornerConfigs[i].stroke = 'transparent';
	        	cornerConfigs[i].strokeWidth = strokeWidth;
	        	
	        	corner = new Kinetic.Line(cornerConfigs[i]);
	
	            corner.on('mouseenter', cornerConfigs[i].onMouseEnterFunc);
	            corner.on('mouseleave', cornerConfigs[i].onMouseLeaveFunc);
	
	            corner.on('dragmove', function () {
	                var boxBounds = getBoundsFromCorner(layer, this.getName());
	
	                box.setPosition(boxBounds.x.min, boxBounds.y.min);
	                box.setSize(boxBounds.x.length, boxBounds.y.length);
	            });
	
	            corner.on('dragend', function () {
	                //--- This can be done on drag end since they're transparent ---//              
	            	setLinesAndCorners(layer, getBoundsFromCorner(layer, this.getName()));
	                layer.draw();
	            });
	
	            layer.add(corner);
	        }
	
	        /*var img2 = img.clone();
	        img2.setName('boxImage');
	        img2.setOffset(0, 0);
	        layer.add(img2);*/
	        stage.add(layer);
	        //boxWindowImageAdjust(box, img, img2);
	        //img2.moveToBottom();
	        layer.moveToTop();
	        layer.draw();
	
	        return layer;
	    }
	    
	    function setBoxDragFuncs(layer, imageLayer) {
	    	var box = layer.get('.windowRect')[0];
	    
	        var anim = new Kinetic.Animation(function(frame) {
	        	//boxWindowImageAdjust(layer.get('.windowRect')[0], imageLayer.get('.image')[0], layer.get('.boxImage')[0]);
	            
	        	/*for (var i = 0; i < boxWindows.length; i++) {
	        		if (boxWindows[i] !== layer) {
	        			boxWindows[i].setAbsolutePosition(layer.getAbsolutePosition());
	        			boxWindows[i].get('.windowRect')[0].setPosition(layer.get('.windowRect')[0].getPosition());
	        			boxWindows[i].get('.windowRect')[0].setSize(layer.get('.windowRect')[0].getSize());
			            boxWindowImageAdjust(boxWindows[i].get('.windowRect')[0], config.layers.bottom[i].get('.image')[0], boxWindows[i].get('.boxImage')[0]);
	        		}
	        	}*/
	        }, boxWindows);
	        
	        box.on('dragstart', function () {
	        	anim.start();
	        });
	        
	        box.on('dragend', function () {
	        	anim.stop();
	        	anim.func();
	        	
	        	//--- This can be done on drag end since they're transparent ---//
	        	for (var i = 0; i < boxWindows.length; i++) {
	        		if (boxWindows[i] !== layer) {
			        	setLinesAndCorners(boxWindows[i], getBounds(boxWindows[i].get('.windowRect')[0]));
			        	boxWindows[i].draw();
	        		}
	        	}
	        	
	        	layer.draw();
	        });
	    }
	    
	    var stage = this.adjustmentSet.stage;
	    var maskLayer = new Kinetic.Layer();
	    
	    
	    maskLayer.add(new Kinetic.Rect({
		    width: stage.getWidth(),
		    height: stage.getHeight(),
		    fill: 'black',
		    opacity: 0.5
	    }))
	    
	    stage.add(maskLayer);
	    
	    var boxWindows = [];
	    boxWindows.push(createBoxWindow(stage, this.adjustmentSet.image));
	    
		setBoxDragFuncs(boxWindows[0], this.adjustmentSet.getLayer());
	    
	    /*Pixastic.process(this.adjustmentSet.getCurrentImage().getImage(), 'desaturate', {}, function(processedImage) {
	    	that.adjustmentSet.image.setImage(processedImage);
			that.adjustmentSet.getLayer().draw();
	    });*/

	    //this.complete();
	}
};

Kinetic.Util.extend(ImageEditing.Crop, ImageEditing.Adjustment);