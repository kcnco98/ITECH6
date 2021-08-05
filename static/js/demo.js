/**
 * demo.js
 * http://www.codrops.com
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 * 
 * Copyright 2016, Codrops
 * http://www.codrops.com
 */
;(function(window) {

	'use strict';

	// taken from mo.js demos
	function isIOSSafari() {
		var userAgent;
		userAgent = window.navigator.userAgent;
		return userAgent.match(/iPad/i) || userAgent.match(/iPhone/i);
	};

	// taken from mo.js demos
	function isTouch() {
		var isIETouch;
		isIETouch = navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0;
		return [].indexOf.call(window, 'ontouchstart') >= 0 || isIETouch;
	};
	
	// taken from mo.js demos
	var isIOS = isIOSSafari(),
		clickHandler = isIOS || isTouch() ? 'touchstart' : 'click';

	function extend( a, b ) {
		for( var key in b ) { 
			if( b.hasOwnProperty( key ) ) {
				a[key] = b[key];
			}
		}
		return a;
	}

	function Animocon(el, options) {
		this.el = el;
		this.options = extend( {}, this.options );
		extend( this.options, options );

		this.checked = false;

		this.timeline = new mojs.Timeline();
		
		for(var i = 0, len = this.options.tweens.length; i < len; ++i) {
			this.timeline.add(this.options.tweens[i]);
		}

		var self = this;
		this.el.addEventListener(clickHandler, function() {
			if( self.checked ) {
				self.options.onUnCheck();
			}
			else {
				self.options.onCheck();
				self.timeline.start();
			}
			self.checked = !self.checked;
		});
	}

	Animocon.prototype.options = {
		tweens : [
			new mojs.Burst({
				shape : 'circle',
				isRunLess: true
			})
		],
		onCheck : function() { return false; },
		onUnCheck : function() { return false; }
	};

	// grid items:
	var items = [].slice.call(document.querySelectorAll('ol.grid > .grid__item'));

//	function init() {
//		/* Icon 1 */
//		var el1 = items[0].querySelector('button.icobutton'), el1span = el1.querySelector('span');
//		new Animocon(el1, {
//			tweens : [
//				// burst animation
//				new mojs.Burst({
//					parent: el1,
//					duration: 1000,
//					shape : 'circle',
//					fill: '#C0C1C3',
//					x: '50%',
//					y: '50%',
//					opacity: 0.6,
//					childOptions: { radius: {15:0} },
//					radius: {30:90},
//					count: 6,
//					isRunLess: true,
//					easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
//				}),
//				// ring animation
//				new mojs.Transit({
//					parent: el1,
//					duration: 700,
//					type: 'circle',
//					radius: {0: 60},
//					fill: 'transparent',
//					stroke: '#C0C1C3',
//					strokeWidth: {20:0},
//					opacity: 0.6,
//					x: '50%',
//					y: '50%',
//					isRunLess: true,
//					easing: mojs.easing.sin.out
//				}),
//				// icon scale animation
//				new mojs.Tween({
//					duration : 1200,
//					onUpdate: function(progress) {
//						if(progress > 0.3) {
//							var elasticOutProgress = mojs.easing.elastic.out(1.43*progress-0.43);
//							el1span.style.WebkitTransform = el1span.style.transform = 'scale3d(' + elasticOutProgress + ',' + elasticOutProgress + ',1)';
//						}
//						else {
//							el1span.style.WebkitTransform = el1span.style.transform = 'scale3d(0,0,1)';
//						}
//					}
//				})
//			],
//			onCheck : function() {
//				el1.style.color = '#988ADE';
//			},
//			onUnCheck : function() {
//				el1.style.color = '#C0C1C3';
//			}
//		});
//		/* Icon 1 */
//
//
//
//		// bursts when hovering the mo.js link
//		var molinkEl = document.querySelector('.special-link'),
//			moTimeline = new mojs.Timeline(),
//			moburst1 = new mojs.Burst({
//				parent: molinkEl,
//				duration: 1300,
//				shape : 'circle',
//				fill : [ '#988ADE', '#DE8AA0', '#8AAEDE', '#8ADEAD', '#DEC58A', '#8AD1DE' ],
//				x: '0%',
//				y: '-50%',
//				radius: {0:60},
//				count: 6,
//				isRunLess: true,
//				easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
//			}),
//			moburst2 = new mojs.Burst({
//				parent: molinkEl,
//				duration: 1600,
//				delay: 100,
//				shape : 'circle',
//				fill : [ '#988ADE', '#DE8AA0', '#8AAEDE', '#8ADEAD', '#DEC58A', '#8AD1DE' ],
//				x: '-100%',
//				y: '-20%',
//				radius: {0:120},
//				count: 14,
//				isRunLess: true,
//				easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
//			}),
//			moburst3 = new mojs.Burst({
//				parent: molinkEl,
//				duration: 1500,
//				delay: 200,
//				shape : 'circle',
//				fill : [ '#988ADE', '#DE8AA0', '#8AAEDE', '#8ADEAD', '#DEC58A', '#8AD1DE' ],
//				x: '130%',
//				y: '-70%',
//				radius: {0:90},
//				count: 8,
//				isRunLess: true,
//				easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
//			}),
//			moburst4 = new mojs.Burst({
//				parent: molinkEl,
//				duration: 2000,
//				delay: 300,
//				shape : 'circle',
//				fill : [ '#988ADE', '#DE8AA0', '#8AAEDE', '#8ADEAD', '#DEC58A', '#8AD1DE' ],
//				x: '-20%',
//				y: '-150%',
//				radius: {0:60},
//				count: 14,
//				isRunLess: true,
//				easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
//			}),
//			moburst5 = new mojs.Burst({
//				parent: molinkEl,
//				duration: 1400,
//				delay: 400,
//				shape : 'circle',
//				fill : [ '#988ADE', '#DE8AA0', '#8AAEDE', '#8ADEAD', '#DEC58A', '#8AD1DE' ],
//				x: '30%',
//				y: '-100%',
//				radius: {0:60},
//				count: 12,
//				isRunLess: true,
//				easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
//			});
//
//		moTimeline.add(moburst1, moburst2, moburst3, moburst4, moburst5);
//		molinkEl.addEventListener('mouseenter', function() {
//			moTimeline.start();
//		});
//	}
//
//	init();

})(window);