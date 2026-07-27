import { n as __exportAll, t as createComponent } from "./compiler_COik8im5.mjs";
import { C as createAstro, _ as addAttribute, a as Fragment, d as renderTemplate, h as maybeRenderHead, i as renderComponent } from "./server_DOagsnPa.mjs";
import { t as $$Layout } from "./Layout_DBRAJ3et.mjs";
import { i as $$Header, n as getCarsByBrand, r as $$Footer } from "./cars_BrK0geLG.mjs";
//#region src/components/AboutInfo.astro
createAstro("https://astro.build");
var $$AboutInfo = createComponent(($$result, $$props, $$slots) => {
	const Astro = $$result.createAstro($$props, $$slots);
	Astro.self = $$AboutInfo;
	const { brand } = Astro.props;
	return renderTemplate`${maybeRenderHead($$result)}<section${addAttribute(`about-${brand}`, "id")} data-astro-cid-ktygg6mk><div class="container" data-astro-cid-ktygg6mk><div class="section-header" data-astro-cid-ktygg6mk>${brand === "suzuki" ? renderTemplate`${renderComponent($$result, "Fragment", Fragment, {}, { "default": ($$result) => renderTemplate`<h2 data-astro-cid-ktygg6mk>About the Suzuki Ignis</h2><p data-astro-cid-ktygg6mk>A stylish and practical compact SUV designed for city driving and weekend adventures.</p>` })}` : renderTemplate`${renderComponent($$result, "Fragment", Fragment, {}, { "default": ($$result) => renderTemplate`<h2 data-astro-cid-ktygg6mk>About the Nissan Cube</h2><p data-astro-cid-ktygg6mk>A quirky and spacious compact hatchback with iconic boxy design and surprising practicality.</p>` })}`}</div><div class="features-grid" data-astro-cid-ktygg6mk>${brand === "suzuki" ? renderTemplate`${renderComponent($$result, "Fragment", Fragment, {}, { "default": ($$result) => renderTemplate`<div class="feature-card" data-astro-cid-ktygg6mk><div class="feature-icon" data-astro-cid-ktygg6mk><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" data-astro-cid-ktygg6mk><circle cx="12" cy="12" r="10" data-astro-cid-ktygg6mk></circle><polyline points="12 6 12 12 16 14" data-astro-cid-ktygg6mk></polyline></svg></div><h3 data-astro-cid-ktygg6mk>Engine & Performance</h3><p data-astro-cid-ktygg6mk>Powered by a 1.2L DualJet petrol engine producing 82 hp, offering a perfect balance of efficiency and responsive city driving.</p></div><div class="feature-card" data-astro-cid-ktygg6mk><div class="feature-icon" data-astro-cid-ktygg6mk><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" data-astro-cid-ktygg6mk><path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z" data-astro-cid-ktygg6mk></path><circle cx="12" cy="10" r="3" data-astro-cid-ktygg6mk></circle></svg></div><h3 data-astro-cid-ktygg6mk>Design & Comfort</h3><p data-astro-cid-ktygg6mk>Bold and modern SUV styling with a raised ground clearance, compact dimensions, and a surprisingly spacious interior for up to 5 passengers.</p></div><div class="feature-card" data-astro-cid-ktygg6mk><div class="feature-icon" data-astro-cid-ktygg6mk><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" data-astro-cid-ktygg6mk><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" data-astro-cid-ktygg6mk></path><circle cx="9" cy="7" r="4" data-astro-cid-ktygg6mk></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87" data-astro-cid-ktygg6mk></path><path d="M16 3.13a4 4 0 0 1 0 7.75" data-astro-cid-ktygg6mk></path></svg></div><h3 data-astro-cid-ktygg6mk>Safety & Reliability</h3><p data-astro-cid-ktygg6mk>Equipped with dual airbags, ABS brakes, and Suzuki's TECT platform for enhanced crash protection. A trusted choice worldwide.</p></div><div class="feature-card" data-astro-cid-ktygg6mk><div class="feature-icon" data-astro-cid-ktygg6mk><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" data-astro-cid-ktygg6mk><rect x="1" y="4" width="22" height="16" rx="2" ry="2" data-astro-cid-ktygg6mk></rect><line x1="1" y1="10" x2="23" y2="10" data-astro-cid-ktygg6mk></line></svg></div><h3 data-astro-cid-ktygg6mk>Fuel Economy</h3><p data-astro-cid-ktygg6mk>Exceptional fuel efficiency averaging 4.9 L/100 km, making it one of the most economical cars to drive in the city and beyond.</p></div>` })}` : renderTemplate`${renderComponent($$result, "Fragment", Fragment, {}, { "default": ($$result) => renderTemplate`<div class="feature-card" data-astro-cid-ktygg6mk><div class="feature-icon" data-astro-cid-ktygg6mk><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" data-astro-cid-ktygg6mk><circle cx="12" cy="12" r="10" data-astro-cid-ktygg6mk></circle><polyline points="12 6 12 12 16 14" data-astro-cid-ktygg6mk></polyline></svg></div><h3 data-astro-cid-ktygg6mk>Engine & Performance</h3><p data-astro-cid-ktygg6mk>Powered by a 1.5L or 1.6L petrol engine, the Cube delivers a smooth and reliable ride perfect for urban commuting.</p></div><div class="feature-card" data-astro-cid-ktygg6mk><div class="feature-icon" data-astro-cid-ktygg6mk><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" data-astro-cid-ktygg6mk><path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z" data-astro-cid-ktygg6mk></path><circle cx="12" cy="10" r="3" data-astro-cid-ktygg6mk></circle></svg></div><h3 data-astro-cid-ktygg6mk>Design & Comfort</h3><p data-astro-cid-ktygg6mk>Iconic asymmetrical rear window and boxy silhouette offer exceptional headroom and a spacious, airy cabin.</p></div><div class="feature-card" data-astro-cid-ktygg6mk><div class="feature-icon" data-astro-cid-ktygg6mk><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" data-astro-cid-ktygg6mk><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" data-astro-cid-ktygg6mk></path><circle cx="9" cy="7" r="4" data-astro-cid-ktygg6mk></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87" data-astro-cid-ktygg6mk></path><path d="M16 3.13a4 4 0 0 1 0 7.75" data-astro-cid-ktygg6mk></path></svg></div><h3 data-astro-cid-ktygg6mk>Safety & Reliability</h3><p data-astro-cid-ktygg6mk>Built with Nissan's reinforced safety cell, front airbags, and side curtain airbags for peace of mind.</p></div><div class="feature-card" data-astro-cid-ktygg6mk><div class="feature-icon" data-astro-cid-ktygg6mk><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" data-astro-cid-ktygg6mk><rect x="1" y="4" width="22" height="16" rx="2" ry="2" data-astro-cid-ktygg6mk></rect><line x1="1" y1="10" x2="23" y2="10" data-astro-cid-ktygg6mk></line></svg></div><h3 data-astro-cid-ktygg6mk>Versatility</h3><p data-astro-cid-ktygg6mk>Modular rear seats fold flat for cargo, making it as practical as it is distinctive — ideal for everyday errands or road trips.</p></div>` })}`}</div></div></section>`;
}, "D:/Final/car_rent-main/src/components/AboutInfo.astro", void 0);
//#endregion
//#region src/components/CarCard.astro
createAstro("https://astro.build");
var $$CarCard = createComponent(($$result, $$props, $$slots) => {
	const Astro = $$result.createAstro($$props, $$slots);
	Astro.self = $$CarCard;
	const { slug, color, model, brand, year, plate, pricePerDay, available, photos } = Astro.props;
	return renderTemplate`${maybeRenderHead($$result)}<a${addAttribute(`/cars/${slug}`, "href")} class="car-card" data-astro-cid-sivy3gub><div class="card-image" data-astro-cid-sivy3gub><img${addAttribute(photos.main, "src")}${addAttribute(`${color} ${brand} ${model} ${year}`, "alt")} width="240" height="180" loading="eager" decoding="async" data-astro-cid-sivy3gub></div><div class="card-info" data-astro-cid-sivy3gub><h3 data-astro-cid-sivy3gub>${color} ${brand} ${model}</h3><span class="plate" data-astro-cid-sivy3gub>${plate}</span><div class="card-footer" data-astro-cid-sivy3gub><span class="price" data-astro-cid-sivy3gub>EC$${pricePerDay}<span data-astro-cid-sivy3gub>/day</span></span>${available ? renderTemplate`<span class="view-btn" data-astro-cid-sivy3gub>View</span>` : renderTemplate`<span class="view-btn disabled" data-astro-cid-sivy3gub>Unavailable</span>`}</div></div></a>`;
}, "D:/Final/car_rent-main/src/components/CarCard.astro", void 0);
//#endregion
//#region src/components/CarGrid.astro
createAstro("https://astro.build");
var $$CarGrid = createComponent(($$result, $$props, $$slots) => {
	const Astro = $$result.createAstro($$props, $$slots);
	Astro.self = $$CarGrid;
	const { brand, cars } = Astro.props;
	const id = brand.toLowerCase();
	return renderTemplate`${maybeRenderHead($$result)}<section${addAttribute(id, "id")} class="car-section" data-astro-cid-islcbanf><div class="galeria-wrapper" data-astro-cid-islcbanf><div class="titulo" data-astro-cid-islcbanf>${brand}<span data-astro-cid-islcbanf>disponibles</span></div><div class="galeria" data-astro-cid-islcbanf>${cars.map((car) => renderTemplate`${renderComponent($$result, "CarCard", $$CarCard, {
		...car,
		"data-astro-cid-islcbanf": true
	})}`)}</div></div></section>`;
}, "D:/Final/car_rent-main/src/components/CarGrid.astro", void 0);
//#endregion
//#region src/pages/index.astro
var pages_exports = /* @__PURE__ */ __exportAll({
	default: () => $$Index,
	file: () => $$file,
	url: () => ""
});
var $$Index = createComponent(($$result, $$props, $$slots) => {
	return renderTemplate`${renderComponent($$result, "Layout", $$Layout, { "data-astro-cid-lcdefpme": true }, { "default": ($$result) => renderTemplate`${renderComponent($$result, "Header", $$Header, { "data-astro-cid-lcdefpme": true })}${maybeRenderHead($$result)}<main data-astro-cid-lcdefpme>${renderComponent($$result, "CarGrid", $$CarGrid, {
		"brand": "Suzuki",
		"cars": getCarsByBrand("Suzuki"),
		"data-astro-cid-lcdefpme": true
	})}${renderComponent($$result, "AboutInfo", $$AboutInfo, {
		"brand": "suzuki",
		"data-astro-cid-lcdefpme": true
	})}${renderComponent($$result, "CarGrid", $$CarGrid, {
		"brand": "Nissan",
		"cars": getCarsByBrand("Nissan"),
		"data-astro-cid-lcdefpme": true
	})}${renderComponent($$result, "AboutInfo", $$AboutInfo, {
		"brand": "nissan",
		"data-astro-cid-lcdefpme": true
	})}</main>${renderComponent($$result, "Footer", $$Footer, { "data-astro-cid-lcdefpme": true })}` })}`;
}, "D:/Final/car_rent-main/src/pages/index.astro", void 0);
var $$file = "D:/Final/car_rent-main/src/pages/index.astro";
//#endregion
//#region \0virtual:astro:page:src/pages/index@_@astro
var page = () => pages_exports;
//#endregion
export { page };
