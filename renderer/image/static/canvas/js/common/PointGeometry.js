var PointGeometry = {
	average: function(pointA, pointB) {
		return {
			x: (pointA.x + pointB.x) / 2,
			y: (pointA.y + pointB.y) / 2
		};
	},
	distance: function(pointA, pointB, scale) {
		if (scale === undefined)
			scale = this.scalarToXYVector(1);
			
		return Math.sqrt(Math.pow((pointB.x - pointA.x) / scale.x, 2) + Math.pow((pointB.y - pointA.y) / scale.y, 2));
	},
	rotation: function(pointA, pointB) {
		return Math.atan2(pointB.y - pointA.y, pointB.x - pointA.x);
	},
	add: function(pointA, pointB) {
		return {
			x: (pointA.x + pointB.x),
			y: (pointA.y + pointB.y)
		};
	},
	subtract: function(pointA, pointB) {
		return {
			x: (pointA.x - pointB.x),
			y: (pointA.y - pointB.y)
		};
	},
	multiply: function(pointA, pointB) {
		return {
			x: (pointA.x * pointB.x),
			y: (pointA.y * pointB.y)
		};
	},
	divide: function(pointA, pointB) {
		return {
			x: (pointA.x / pointB.x),
			y: (pointA.y / pointB.y)
		};
	},
	scalarToXYVector: function(scalar) {
		return {
			x: scalar,
			y: scalar
		};
	}
};