
FirstGame.Preloader = function (game) {

	this.preloadBar = null;

	this.ready = false;

};

FirstGame.Preloader.prototype = {

	preload: function () {

		//	These are the assets we loaded in Boot.js
		//	A nice sparkly background and a loading progress bar
		this.preloadBar = this.add.sprite(this.game.world.width/2 - this.cache.getImage('preloaderBar').width/2,this.game.world.height/2 - this.cache.getImage('preloaderBar').height/2, 'preloaderBar');

		//	This sets the preloadBar sprite as a loader sprite.
		//	What that does is automatically crop the sprite from 0 to full-width
		//	as the files below are loaded in.
		this.load.setPreloadSprite(this.preloadBar);

		//	Here we load the rest of the assets our game needs.
		//	As this is just a Project Template I've not provided these assets, swap them for your own.
		//this.load.image('titlepage', 'images/title.jpg');
		//this.load.atlas('playButton', 'images/play_button.png', 'images/play_button.json');
		//this.load.audio('titleMusic', ['audio/main_menu.mp3']);
		//this.load.bitmapFont('caslon', 'fonts/caslon.png', 'fonts/caslon.xml');
		//	+ lots of other required assets here
        
        this.game.stage.backgroundColor = '#000011';
        this.load.image('logo','img/Phaser-Logo-Small.png');
        
        
        this.load.image('SpaceShip','img/ship.png');
        this.load.image('Star','img/star.png');
        
        this.load.audio('backgroundMusic', ["audio/creep.mp3","audio/creep.ogg"]);
        this.load.audio('catchStarSound', "audio/dropmetalthing.ogg");
        
        this.load.image('arrow', 'img/ui/icon-green-arrow.png');
        this.load.image('toppanel', 'img/ui/staroverflow_gui_1.png');
        this.load.image('leftpanel', 'img/ui/staroverflow_gui_2.png');
        this.load.image('rightpanel', 'img/ui/staroverflow_gui_3.png');
        this.load.image('bottompanel', 'img/ui/staroverflow_gui_4.png');
        
        this.load.spritesheet('pausebutton', 'img/ui/pausebutton.png', 161, 43, 2);
        
        this.load.bitmapFont('coalition','font/font.png','font/font.fnt');
        
        this.load.spritesheet('lowbutton', 'img/ui/lowerbutton.png', 304, 54, 2);

	},

	create: function () {

		//	Once the load has finished we disable the crop because we're going to sit in the update loop for a short while as the music decodes
		this.preloadBar.cropEnabled = false;

	},

	update: function () {

		//	You don't actually need to do this, but I find it gives a much smoother game experience.
		//	Basically it will wait for our audio file to be decoded before proceeding to the MainMenu.
		//	You can jump right into the menu if you want and still play the music, but you'll have a few
		//	seconds of delay while the mp3 decodes - so if you need your music to be in-sync with your menu
		//	it's best to wait for it to decode here first, then carry on.
		
		//	If you don't have any music in your game then put the game.state.start line into the create function and delete
		//	the update function completely.
		
		if (this.cache.isSoundDecoded('backgroundMusic') && this.cache.isSoundDecoded('catchStarSound') && this.ready == false)
		{
			this.ready = true;
			this.state.start('Main');
		}

	}

};