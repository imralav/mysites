FirstGame.Game = function (game) {
    
};

var music;
var catchStarSound;

//score
var score = 0;
var scoreText;

var money = 0;
var moneyText;

var starsAmount = 0;
var starsAmountText;

var timeText;

var pauseText;
var pauseTriggerText;

var gameOverText;

var increaseStarText;
var increaseStarCost = 10;
var increaseShipText;
var increaseShipCost = 10;
var increaseStarCapacityText;
var increaseStarCapacityCost = 10;
var INITIAL_COST = 10;

var spaceShip;
var stars;
var INITIAL_STARS_AMOUNT = 10;
var SPACE_OFFSET = 100;
var STAR_MAX_SPEED = 100;
var STAR_MIN_SPEED = 25;
var STAR_MAX_AMOUNT = 30;
var INITIAL_STAR_CAPACITY_AMOUNT = 30;
var STAR_MAX_SCALE = 1.0;
var STAR_MIN_SCALE = 0.5;
var STAR_SCALE = 0.5;
var SPACESHIP_SCALE = 1.0;
var MAX_SPACESHIP_SCALE = 2.0;
var MIN_SPACESHIP_SCALE = 1.0;
var STAR_INCREASE_FACTOR = 0.1;
var SHIP_INCREASE_FACTOR = 0.1;
var STAR_CAPACITY_INCREASE_FACTOR = 10;
var STAR_INCREASE_COST_FACTOR = 1.5;
var SHIP_INCREASE_COST_FACTOR = 1.5;
var STAR_CAPACITY_INCREASE_COST_FACTOR = 1.5;

var gameOver = false;

var isPaused = false;

var borders;

var pauseButton;

var uiElements;

var increaseStarButton;
var increaseStarCapacityButton;
var increaseShipButton;


FirstGame.Game.prototype = {
    
    initiateTextFields: function () {
        scoreText = this.game.add.bitmapText(825,4,'coalition','SCORE: 0',20);
        
        moneyText = this.game.add.bitmapText(825,25,'coalition','MONEY: 0', 20);
        
        starsAmountText = this.game.add.bitmapText(125,15,'coalition','STARS: ' + starsAmount + '/' + STAR_MAX_AMOUNT, 20);
        
        timeText = this.game.add.bitmapText(563,15,'coalition',this.lastTime - this.beginTime, 20);
        
        pauseText = this.game.add.bitmapText(this.game.world.width/2-50,this.game.world.height/2,'coalition',"", 24);
        
        gameOverText = this.game.add.bitmapText(this.game.world.width/2-250, this.game.world.height/2, 'coalition', "", 24);
        
        increaseShipText = this.game.add.bitmapText(480, this.game.world.height-60,'coalition',"Increase ship's size ("+increaseShipCost+")", 12);
        increaseShipText.inputEnabled = true;
        increaseShipText.events.onInputUp.add(this.increaseShip,this);
        
        increaseStarText = this.game.add.bitmapText(130, this.game.world.height-60, 'coalition', "Increase stars size ("+increaseStarCost+")", 12);
        increaseStarText.inputEnabled = true;
        increaseStarText.events.onInputUp.add(this.increaseStar,this);
        
        increaseStarCapacityText = this.game.add.bitmapText(815, this.game.world.height-60, 'coalition', "Increase stars capacity ("+increaseStarCapacityCost+")", 12);
        increaseStarCapacityText.inputEnabled = true;
        increaseStarCapacityText.events.onInputUp.add(this.increaseStarCapacity,this);
        
    },
    
    increaseStarCapacity: function () {
        if(money >= increaseStarCapacityCost) {
            money-=increaseStarCapacityCost;
            STAR_MAX_AMOUNT+=STAR_CAPACITY_INCREASE_FACTOR;
            increaseStarCapacityCost*=STAR_CAPACITY_INCREASE_COST_FACTOR;
            increaseStarCapacityCost=parseInt(increaseStarCapacityCost);
            increaseStarCapacityText.setText("Increase stars capacity ("+increaseStarCapacityCost+")");
        }
    },
    
    increaseStar: function() {
        if(STAR_SCALE < STAR_MAX_SCALE && money >= increaseStarCost) {
            money-=increaseStarCost;
            STAR_SCALE+=STAR_INCREASE_FACTOR;
            for(var i = 0; i<stars.length; i++) {
                this.game.add.tween(stars.getAt(i).scale).to({x:STAR_SCALE, y:STAR_SCALE},1500, Phaser.Easing.Bounce.Out,true);    
            }
            increaseStarCost*=STAR_INCREASE_COST_FACTOR;
            increaseStarCost = parseInt(increaseStarCost);
            increaseStarText.setText("Increase stars size ("+increaseStarCost+")");
        }
        if(STAR_SCALE >= STAR_MAX_SCALE) {
            increaseStarText.setText("Star size maxed.");
        }
    },
    
    increaseShip: function () {
        if(SPACESHIP_SCALE < MAX_SPACESHIP_SCALE && money >= increaseShipCost) {
            money-=increaseShipCost;
            SPACESHIP_SCALE+=SHIP_INCREASE_FACTOR;
            this.game.add.tween(spaceShip.scale).to({x: SPACESHIP_SCALE, y: SPACESHIP_SCALE},1500, Phaser.Easing.Bounce.Out, true);
            increaseShipCost*=SHIP_INCREASE_COST_FACTOR;
            increaseShipCost = parseInt(increaseShipCost);
            increaseShipText.setText("Increase ship's size ("+increaseShipCost+")");
        }
        if(SPACESHIP_SCALE >= MAX_SPACESHIP_SCALE) 
        {
            increaseShipText.setText("Ship's size maxed.");
        }
    },
    
    initiateStars: function (initialStarsAmount) {
        starsAmount = 0;
        this.createStar(initialStarsAmount);
    },
    
    initiateSpaceShip: function() {
        spaceShip = this.game.add.sprite(this.game.world.centerX,this.game.world.centerY,'SpaceShip');
        spaceShip.anchor.set(0.5);
        spaceShip.angle = 90;
        
        this.game.physics.arcade.enable(spaceShip);
        spaceShip.body.collideWorldBounds = true;
        spaceShip.body.bounce.x = 1;
        spaceShip.body.bounce.y = 1;
    },
    
    preload: function() {
    },
        
    create: function() {
        this.beginTime = this.game.time.now;
        this.lastTime = this.game.time.now;
        this.game.physics.startSystem(Phaser.Physics.ARCADE);
        
        uiElements = this.game.add.group();
        uiElements.enableBody = true;
        
        var uiElem = uiElements.create(0,0,'toppanel');
        uiElem.body.immovable = true;
        uiElem = uiElements.create(0,this.game.cache.getImage('toppanel').height,'leftpanel');
        uiElem.body.immovable = true;
        uiElem = uiElements.create(this.game.world.width - this.game.cache.getImage('rightpanel').width, this.game.cache.getImage('toppanel').height,'rightpanel');
        uiElem.body.immovable = true;
        uiElem = uiElements.create(0,this.game.world.height-this.game.cache.getImage('bottompanel').height, 'bottompanel');
        uiElem.body.immovable = true;
        
        this.initiateSpaceShip();
        
        stars = this.game.add.group();
        stars.enableBody = true;
        
        increaseStarButton = this.game.add.button(96, this.game.world.height - 96 + 18, 'lowbutton', this.increaseStar,this,0, 1, 1);
        
        increaseShipButton = this.game.add.button(448, this.game.world.height - 96 + 18, 'lowbutton', this.increaseShip,this,0, 1, 1);
        
        increaseStarCapacityButton = this.game.add.button(792, this.game.world.height - 96 + 18, 'lowbutton', this.increaseStarCapacity,this,0, 1, 1);

        this.initiateTextFields();
        
        this.initiateStars(INITIAL_STARS_AMOUNT);
        
        this.timer = this.game.time.events.loop(1500, function() {this.createStar(1+0.3*Math.ceil((this.lastTime - this.beginTime)/5000))}, this);
        
        //this.game.input.onDown.add(function(event) {this.unpause()},this);
        
        music = this.game.add.audio('backgroundMusic', 1, true);
        music.play();
        
        catchStarSound = this.game.add.audio('catchStarSound');
        catchStarSound.volume *= 0.3;
        
        pauseButton = this.game.add.button(this.game.world.width/2, this.game.cache.getImage('toppanel').height+22,'pausebutton',this.pauseTrigger,this,1,0,1);
        pauseButton.anchor.set(0.5);
        

    },
        
    update: function () {
        if(isPaused == false) {
            this.lastTime+=this.game.time.elapsed;
            var currentTime = (this.lastTime - this.beginTime)/1000
            var minutes = Math.floor(currentTime/60);
            if(minutes < 10)
                minutes = '0' + minutes;
            var seconds = Math.floor(currentTime)%60;
            if(seconds < 10)
                seconds = '0' + seconds;
            timeText.setText(minutes +':'+seconds);
            scoreText.setText('SCORE: ' + score);
            moneyText.setText('MONEY: ' + money);
            if(this.game.input.activePointer.x > 55 && this.game.input.activePointer.x < this.game.world.width - 55
               && this.game.input.activePointer.y > 55 && this.game.input.activePointer.y < this.game.world.height - 100) {
                this.game.physics.arcade.moveToPointer(spaceShip, 60, this.game.input.activePointer, 500);
            }
            spaceShip.rotation = this.game.physics.arcade.angleToPointer(spaceShip) + Math.PI/2;

            this.game.physics.arcade.overlap(spaceShip, stars, this.collectStar, null, this);
            if(starsAmount < 60)
                this.game.physics.arcade.collide(stars,stars);
            
            if(starsAmount > STAR_MAX_AMOUNT) {
                this.gameOver();
            }
        }
        this.game.physics.arcade.collide(uiElements,stars);
        this.game.physics.arcade.collide(spaceShip, uiElements);
    },
    
    collectStar: function (spaceShip, star) {
        score++;
        scoreText.setText('SCORE: '+score);

        money++;
        moneyText.setText('MONEY: '+money);

        star.kill();

        if(starsAmount > 0) {
            starsAmount--;
            starsAmountText.setText('STARS: ' + starsAmount + '/' + STAR_MAX_AMOUNT);
        }
        
        catchStarSound.play();
    },
    
    createStar: function(amount) {
        if(!isPaused) {
            for(var i = 0; i<amount; i++) {
                var star = stars.create(SPACE_OFFSET + Math.random() * (this.game.world.width-this.game.cache.getImage('Star').width - 2*SPACE_OFFSET), SPACE_OFFSET + Math.random() * (this.game.world.height - this.game.cache.getImage('Star').height - 2*SPACE_OFFSET), 'Star');
                //star.body.gravity.y = 300;
                star.body.bounce.y = 1;
                star.body.bounce.x = 1;
                star.body.velocity.x = 2*STAR_MAX_SPEED * Math.random() - STAR_MAX_SPEED;
                star.body.velocity.y = 2*STAR_MAX_SPEED * Math.random() - STAR_MAX_SPEED; 
                star.body.collideWorldBounds = true;
                starsAmount++;
                starsAmountText.setText('STARS: ' + starsAmount + '/' + STAR_MAX_AMOUNT);
                star.scale.set(STAR_MIN_SCALE,STAR_MIN_SCALE);
                this.game.add.tween(star.scale).to({x: STAR_SCALE, y: STAR_SCALE},1500, Phaser.Easing.Bounce.Out, true);
            }
        }
    },
    
    pause: function(event) {
        if(!isPaused) {
            isPaused = true;
            pauseText.setText("PAUSED");
            music.pause();
        }
    },
    
    unpause: function(event) {
        if(gameOver) {
            gameOver = false;
            gameOverText.setText("");
            isPaused = false;
            this.resetGame.call(this);
            music.resume();
        }
        else
            if(isPaused) {
                isPaused = false;
                pauseText.setText("");
                music.resume();
            }
    },
    
    pauseTrigger: function() {
        if(isPaused) {
            pauseButton.setFrames(1,0,0);
            this.unpause();
        }
        else {
            pauseButton.setFrames(0,1,1);
            this.pause();
        }
    },
    
    gameOver: function () {
        isPaused = true;
        gameOver = true;
        gameOverText.setText("Game Over! Click anywhere to restart.");
        this.game.input.onDown.addOnce(this.unpause,this);
    },
    
    resetGame: function() {
        STAR_SCALE = STAR_MIN_SCALE;
        SPACESIP_SCALE = MIN_SPACESHIP_SCALE;
        STAR_MAX_AMOUNT = INITIAL_STAR_CAPACITY_AMOUNT;
        increaseShipCost = INITIAL_COST;
        increaseStarCapacityCost = INITIAL_COST;
        increaseStarCost = INITIAL_COST;
        spaceShip.scale.set(SPACESHIP_SCALE,SPACESHIP_SCALE);
        stars.removeAll();
        this.initiateStars(INITIAL_STARS_AMOUNT);
        score = 0;
        money = 0;
        this.beginTime = this.game.time.now;
        this.lastTime = this.game.time.now;
        increaseStarCapacityText.setText("Increase stars capacity ("+increaseStarCapacityCost+")");
        increaseStarText.setText("Increase stars size ("+increaseStarCost+")");
        increaseShipText.setText("Increase ship's size ("+increaseShipCost+")");
    },
    
    render: function() {
        //this.game.debug.renderSoundInfo(catchStarSound,20,20);    
    }
};
