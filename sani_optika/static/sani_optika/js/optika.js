function onload(event) {


	var starRating1 = raterJs({
		starSize:16,
		element: document.querySelector('[id^="rater-"]'),
		rateCallback:function rateCallback(rating, done) {

			var data = {
				'rating': rating
			}
			console.log(this);

			this.setRating(rating);
			done();
		}
	});


}

window.addEventListener("load", onload, false);
