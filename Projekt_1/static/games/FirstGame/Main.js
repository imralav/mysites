

FirstGame.Main = function (game) {
    
};

FirstGame.Main.prototype = {
    preload: function() {
    },
    
    create: function () {
        var image = this.game.add.sprite(this.world.centerX,this.world.centerY,'logo');
        image.anchor.set(0.5);
        image.scale.setTo(0.0,0.0);
        var tween = this.game.add.tween(image.scale).to({x: 1.0,y: 1.0},500,Phaser.Easing.Bounce.Out, true);
        tween.onComplete.add(this.tweenFinished,this);
    },
    tweenFinished: function() {
        this.game.state.start('Game');   
    },
    
    update: function () {
        
    }
};