<!DOCTYPE html>

<!--  
   GLmol - Molecular Viewer on WebGL/Javascript 

   (C) Copyright 2011, biochem_fan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    This program uses
      Three.js 
         https://github.com/mrdoob/three.js
         Copyright (c) 2010-2011 three.js Authors. All rights reserved.
      jQuery
         http://jquery.org/
         Copyright (c) 2011 John Resig
-->

<html>

<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, target-densitydpi=device-dpi">

  <meta charset="utf-8">

  <title>GLmol embedding examples</title>
  <style type="text/css">
  </style>

  <script src="/static/pdb/js/jquery-1.7.min.js"></script>
  <script src="/static/pdb/js/Three49custom.js"></script>
  <script type="text/javascript" src="/static/pdb/js/GLmol.js"></script>
</head>

<body>
<h1>GLmol embedding</h1>
<p>You can embed multiple instances of GLmol in a page. Molecular representations can be customized by Javascript. For the details, please examine the source code of this page. If it is not clear, don't hesitate to ask me (biochem_fan at users.sourceforge.jp).</p>

<p>Rotation: left button, Translation: middle button or Ctrl-key + left button, Zoom: Wheel or right button(up/down) or Shift-key + left button(up/down)</p>

<div id="glmol01" style="width: 500px; height: 400px; background-color: black;"></div> 
<textarea id="glmol01_src" style="display: none;">
  ${ pdb_file }
</textarea>

<script type="text/javascript">
var glmol01 = new GLmol('glmol01', true);

glmol01.defineRepresentation = function() {
  var all = this.getAllAtoms();
  var hetatm = this.removeSolvents(this.getHetatms(all));
  this.colorByAtom(all, {});
  this.colorByChain(all);

  var asu = new THREE.Object3D(); 
  this.drawBondsAsStick(
    asu, 
    hetatm, 
    this.cylinderRadius, 
    this.cylinderRadius
  );
  this.drawBondsAsStick(
    asu, 
    this.getResiduesById(this.getSidechains(this.getChain(all, ['A'])), [58, 87]), 
    this.cylinderRadius, 
    this.cylinderRadius
  );
  this.drawBondsAsStick(
    asu, 
    this.getResiduesById(
      this.getSidechains(this.getChain(all, ['B'])), [63, 92]), this.cylinderRadius, this.cylinderRadius);
    this.drawCartoon(asu, all, this.curveWidth, this.thickness
  );
  this.drawSymmetryMates2(
    this.modelGroup, 
    asu, 
    this.protein.biomtMatrices
  );
  this.modelGroup.add(asu);
};

glmol01.loadMolecule();
</script>

<hr style="clear: both;">
<br>(C) Copyright 2011 biochem_fan (biochem_fan at users.sourceforge.jp). <br>
<p>This program is released under LGPL3.</p>
</body>

</html>
