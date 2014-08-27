<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, target-densitydpi=device-dpi">

<meta charset="utf-8">

<style type="text/css">
</style>
<div id="errorDisp"></div>
<div id="glmol01" style="width: 500px; height: 400px; background-color: black; display:none;"></div>
<textarea id="glmol01_src" style="display: none;">
  ${ pdb_file }
</textarea>

<script type="text/javascript">
(function(){
    try{
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

            $("#glmol01").css({"display": "block"})
        };

    glmol01.loadMolecule();
}
    catch(e){
        $("#glmol01").remove();
        $("#errorDisp").html('File did not render properly. Try finding a current version on the <a href="http://www.rcsb.org/pdb/home/home.do">Protein Data Bank</a>');
    }
})();
</script>
