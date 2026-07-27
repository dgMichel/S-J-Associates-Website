import { n as __exportAll, t as createComponent } from "./compiler_COik8im5.mjs";
import { C as createAstro, _ as addAttribute, d as renderTemplate, h as maybeRenderHead, i as renderComponent } from "./server_DOagsnPa.mjs";
import { n as renderScript, t as $$Layout } from "./Layout_DBRAJ3et.mjs";
import { i as $$Header, r as $$Footer, t as cars } from "./cars_BrK0geLG.mjs";
//#region src/components/Booking.astro
createAstro("https://astro.build");
var $$Booking = createComponent(($$result, $$props, $$slots) => {
	const Astro = $$result.createAstro($$props, $$slots);
	Astro.self = $$Booking;
	const { car } = Astro.props;
	const safeCar = car ?? {
		slug: "",
		brand: "Vehicle",
		model: "Unavailable",
		pricePerDay: 0
	};
	return renderTemplate`${maybeRenderHead($$result)}<section class="booking-section" id="booking" data-astro-cid-5n25xmrl><div class="booking-container" data-astro-cid-5n25xmrl><div class="booking-header" data-astro-cid-5n25xmrl><h2 data-astro-cid-5n25xmrl>Book via WhatsApp</h2><p class="booking-subtitle" data-astro-cid-5n25xmrl>Send your booking request via WhatsApp</p></div><div class="booking-form" data-astro-cid-5n25xmrl><div class="days-selector" data-astro-cid-5n25xmrl><label for="dayCount" data-astro-cid-5n25xmrl>Number of days</label><input id="dayCount" class="days-input" type="number" min="1" placeholder="1" inputmode="numeric" data-astro-cid-5n25xmrl></div><div class="days-selector deposit-selector" data-astro-cid-5n25xmrl><label data-astro-cid-5n25xmrl>Client type</label><div class="deposit-options" data-astro-cid-5n25xmrl><label data-astro-cid-5n25xmrl><input type="radio" name="nationality" id="nationalRadio" value="national" checked data-astro-cid-5n25xmrl> National (EC$ 500)</label><label data-astro-cid-5n25xmrl><input type="radio" name="nationality" id="foreignRadio" value="foreign" data-astro-cid-5n25xmrl> Foreign (US$350)</label></div></div><div class="price-breakdown" data-astro-cid-5n25xmrl><div class="price-row" data-astro-cid-5n25xmrl><span data-astro-cid-5n25xmrl>EC$ ${safeCar.pricePerDay} &times; <span id="calcDays" data-astro-cid-5n25xmrl>1</span> day(s)</span><span id="subtotal" data-astro-cid-5n25xmrl>EC$ ${safeCar.pricePerDay}</span></div><div class="price-row deposit-row" data-astro-cid-5n25xmrl><span data-astro-cid-5n25xmrl>Security Deposit</span><span id="depositAmt" data-astro-cid-5n25xmrl>EC$ 500</span></div><div class="price-row total" data-astro-cid-5n25xmrl><span data-astro-cid-5n25xmrl>Total</span><span id="total" data-astro-cid-5n25xmrl>EC$ ${safeCar.pricePerDay} + Security Deposit</span></div></div><a id="whatsappBtn" class="pay-btn whatsapp-btn"${addAttribute(`https://wa.me/14734036877?text=${encodeURIComponent(`Hola, quiero reservar el auto ${safeCar.brand} ${safeCar.model}`)}`, "href")} target="_blank" rel="noreferrer noopener" data-astro-cid-5n25xmrl>Contact via WhatsApp</a></div></div><div id="bookingData"${addAttribute(safeCar.slug, "data-slug")}${addAttribute(safeCar.pricePerDay, "data-price")}${addAttribute(safeCar.brand, "data-brand")}${addAttribute(safeCar.model, "data-model")} style="display:none" data-astro-cid-5n25xmrl></div></section>${renderScript($$result, "D:/Final/car_rent-main/src/components/Booking.astro?astro&type=script&index=0&lang.ts")}`;
}, "D:/Final/car_rent-main/src/components/Booking.astro", void 0);
//#endregion
//#region src/pages/cars/[slug].astro
var _slug__exports = /* @__PURE__ */ __exportAll({
	default: () => $$Slug,
	file: () => $$file,
	getStaticPaths: () => getStaticPaths,
	url: () => $$url
});
createAstro("https://astro.build");
function getStaticPaths() {
	return cars.map((car) => ({
		params: { slug: car.slug },
		props: { car }
	}));
}
var $$Slug = createComponent(($$result, $$props, $$slots) => {
	const Astro = $$result.createAstro($$props, $$slots);
	Astro.self = $$Slug;
	const { car } = Astro.props;
	const safeCar = car ?? {
		slug: "",
		brand: "Vehicle",
		model: "Unavailable",
		color: "",
		plate: "",
		description: "This vehicle is currently unavailable.",
		year: "",
		pricePerDay: 0,
		photos: {},
		specs: {
			engine: "",
			transmission: "",
			fuel: "",
			seats: "",
			doors: ""
		},
		features: []
	};
	const photos = safeCar.photos ?? {};
	const views = [
		{
			key: "front",
			label: "Front"
		},
		{
			key: "side",
			label: "Side"
		},
		{
			key: "back",
			label: "Back"
		}
	];
	return renderTemplate`${renderComponent($$result, "Layout", $$Layout, { "data-astro-cid-flotoib7": true }, { "default": ($$result) => renderTemplate`${renderComponent($$result, "Header", $$Header, { "data-astro-cid-flotoib7": true })}${maybeRenderHead($$result)}<main class="detail-page" data-astro-cid-flotoib7><div class="container" data-astro-cid-flotoib7><a href="/" class="back-link" data-astro-cid-flotoib7>&larr; Back to fleet</a><div class="detail-grid" data-astro-cid-flotoib7><div class="gallery" data-astro-cid-flotoib7><div class="gallery-stage" data-astro-cid-flotoib7><div class="main-image" data-astro-cid-flotoib7><img${addAttribute(photos.front || "", "src")}${addAttribute(`${safeCar.color} ${safeCar.brand} ${safeCar.model}`, "alt")} width="400" height="300" loading="lazy" data-astro-cid-flotoib7></div><div class="gallery-floor" data-astro-cid-flotoib7></div></div><div class="thumbnails" data-astro-cid-flotoib7>${views.map((view) => renderTemplate`<button class="thumb"${addAttribute(view.key, "data-view")} data-astro-cid-flotoib7><img${addAttribute(photos[view.key] || photos.front || "", "src")}${addAttribute(`${view.label} view`, "alt")} width="100" height="80" loading="lazy" data-astro-cid-flotoib7><span data-astro-cid-flotoib7>${view.label}</span></button>`)}</div></div><div class="info" data-astro-cid-flotoib7><div class="info-header" data-astro-cid-flotoib7><h1 data-astro-cid-flotoib7>${safeCar.color} ${safeCar.brand} ${safeCar.model}</h1><span class="plate" data-astro-cid-flotoib7>${safeCar.plate}</span></div><p class="description" data-astro-cid-flotoib7>${safeCar.description}</p><div class="specs" data-astro-cid-flotoib7><h3 data-astro-cid-flotoib7>Specifications</h3><div class="specs-grid" data-astro-cid-flotoib7><div class="spec-item" data-astro-cid-flotoib7><span class="spec-label" data-astro-cid-flotoib7>Year</span><span class="spec-value" data-astro-cid-flotoib7>${safeCar.year}</span></div><div class="spec-item" data-astro-cid-flotoib7><span class="spec-label" data-astro-cid-flotoib7>Engine</span><span class="spec-value" data-astro-cid-flotoib7>${safeCar.specs?.engine}</span></div><div class="spec-item" data-astro-cid-flotoib7><span class="spec-label" data-astro-cid-flotoib7>Transmission</span><span class="spec-value" data-astro-cid-flotoib7>${safeCar.specs?.transmission}</span></div><div class="spec-item" data-astro-cid-flotoib7><span class="spec-label" data-astro-cid-flotoib7>Fuel</span><span class="spec-value" data-astro-cid-flotoib7>${safeCar.specs?.fuel}</span></div><div class="spec-item" data-astro-cid-flotoib7><span class="spec-label" data-astro-cid-flotoib7>Seats</span><span class="spec-value" data-astro-cid-flotoib7>${safeCar.specs?.seats}</span></div><div class="spec-item" data-astro-cid-flotoib7><span class="spec-label" data-astro-cid-flotoib7>Doors</span><span class="spec-value" data-astro-cid-flotoib7>${safeCar.specs?.doors}</span></div></div></div><div class="features" data-astro-cid-flotoib7><h3 data-astro-cid-flotoib7>Features</h3><div class="features-list" data-astro-cid-flotoib7>${(safeCar.features ?? []).map((f) => renderTemplate`<span class="feature-tag" data-astro-cid-flotoib7>${f}</span>`)}</div></div><div class="price-box" data-astro-cid-flotoib7><div class="price-main" data-astro-cid-flotoib7><div data-astro-cid-flotoib7><span class="price-amount" data-astro-cid-flotoib7>EC$${safeCar.pricePerDay}</span><span class="price-period" data-astro-cid-flotoib7>per day</span></div></div><div class="security-deposit" data-astro-cid-flotoib7><div class="deposit-header" data-astro-cid-flotoib7><span class="deposit-icon" data-astro-cid-flotoib7>🔒</span><h4 data-astro-cid-flotoib7>Refundable Security Deposit</h4></div><ul class="deposit-list" data-astro-cid-flotoib7><li data-astro-cid-flotoib7>EC$500 for local residents</li><li data-astro-cid-flotoib7>US$350 for international visitors</li></ul><p class="deposit-note" data-astro-cid-flotoib7>The security deposit is fully refundable upon return of the vehicle, provided it is returned in the same condition and no additional charges apply.</p></div><p class="price-note" data-astro-cid-flotoib7>Long-term rentals are available at discounted rates. Contact us for a personalized quote.</p></div>${renderComponent($$result, "Booking", $$Booking, {
		"car": safeCar,
		"data-astro-cid-flotoib7": true
	})}</div></div></div></main>${renderComponent($$result, "Footer", $$Footer, { "data-astro-cid-flotoib7": true })}` })}${renderScript($$result, "D:/Final/car_rent-main/src/pages/cars/[slug].astro?astro&type=script&index=0&lang.ts")}`;
}, "D:/Final/car_rent-main/src/pages/cars/[slug].astro", void 0);
var $$file = "D:/Final/car_rent-main/src/pages/cars/[slug].astro";
var $$url = "/cars/[slug]";
//#endregion
//#region \0virtual:astro:page:src/pages/cars/[slug]@_@astro
var page = () => _slug__exports;
//#endregion
export { page };
