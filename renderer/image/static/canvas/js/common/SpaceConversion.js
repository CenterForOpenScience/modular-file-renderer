function toImageSpace(pointPosition, image) {
	var imageScale;
	
	if (image.scale === undefined) {
		imageScale = image.getScale();
	} else {
		imageScale = image.scale;
	}
	
	return {
		x: image.isFlippedHorizontally ? image.originalSize.width - pointPosition.x / imageScale.x : pointPosition.x / imageScale.x,
		y: image.isFlippedVertically ? image.originalSize.height - pointPosition.y / imageScale.y : pointPosition.y / imageScale.y
	};
}

function toCanvasSpace(pointPosition, image) {
	var imageScale;
	
	if (image.scale === undefined) {
		imageScale = image.getScale();
	} else {
		imageScale = image.scale;
	}

	return {
		x: (image.isFlippedHorizontally ? image.originalSize.width - pointPosition.x : pointPosition.x) * imageScale.x,
		y: (image.isFlippedVertically ? image.originalSize.height - pointPosition.y : pointPosition.y) * imageScale.y
	};
}

function getRotatedSize(size, rotation) {
	var absCosRotation = Math.abs(Math.cos(rotation)),
		absSinRotation = Math.abs(Math.sin(rotation));
	
    return {
        width: size.width * absCosRotation + size.height * absSinRotation,
        height: size.width * absSinRotation + size.height * absCosRotation
    };
}

function toRotatedImageSpace(point, origSize, newSize, rotation) {
	return {
		x: (Math.cos(rotation) * (point.x - origSize.width / 2) - Math.sin(rotation) * (point.y - origSize.height / 2)) + newSize.width / 2,
		y: (Math.sin(rotation) * (point.x - origSize.width / 2) + Math.cos(rotation) * (point.y - origSize.height / 2)) + newSize.height / 2
	};
}

function toRotatedGroupSpace(groupPosition, imagePosition, rotation) {
	var delta = {
		x: imagePosition.x - groupPosition.x,
		y: imagePosition.y - groupPosition.y
	};
	
	return {
		x: Math.cos(rotation) * delta.x - Math.sin(rotation) * delta.y + groupPosition.x,
		y: Math.sin(rotation) * delta.x + Math.cos(rotation) * delta.y + groupPosition.y
	};
}

function getRotatedSize(size, rotation) {
	var absCosRotation = Math.abs(Math.cos(rotation)),
		absSinRotation = Math.abs(Math.sin(rotation));
	
    return {
        width: size.width * absCosRotation + size.height * absSinRotation,
        height: size.width * absSinRotation + size.height * absCosRotation
    };
}