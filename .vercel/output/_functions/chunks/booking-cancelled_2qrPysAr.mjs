import { n as __exportAll, t as createComponent } from "./compiler_COik8im5.mjs";
import { d as renderTemplate, h as maybeRenderHead, i as renderComponent } from "./server_DOagsnPa.mjs";
import { t as $$Layout } from "./Layout_DBRAJ3et.mjs";
//#region src/pages/booking-cancelled.astro
var booking_cancelled_exports = /* @__PURE__ */ __exportAll({
	default: () => $$BookingCancelled,
	file: () => $$file,
	url: () => $$url
});
var $$BookingCancelled = createComponent(($$result, $$props, $$slots) => {
	return renderTemplate`${renderComponent($$result, "Layout", $$Layout, {}, { "default": ($$result) => renderTemplate`${maybeRenderHead($$result)}<main style="min-height:80vh;display:flex;align-items:center;justify-content:center;padding:48px 24px"><div style="text-align:center;max-width:480px"><div style="width:64px;height:64px;border-radius:50%;background:#fef2f2;display:flex;align-items:center;justify-content:center;margin:0 auto 24px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></div><h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:8px">Payment Cancelled</h1><p style="font-size:15px;color:#64748b;line-height:1.7;margin-bottom:32px">Your payment was not completed. No charges have been made. You can try again whenever you're ready.</p><a href="/" style="display:inline-flex;padding:14px 32px;background:#0f172a;color:white;border-radius:12px;font-size:15px;font-weight:600;text-decoration:none">Back to Home</a></div></main>` })}`;
}, "D:/Final/car_rent-main/src/pages/booking-cancelled.astro", void 0);
var $$file = "D:/Final/car_rent-main/src/pages/booking-cancelled.astro";
var $$url = "/booking-cancelled";
//#endregion
//#region \0virtual:astro:page:src/pages/booking-cancelled@_@astro
var page = () => booking_cancelled_exports;
//#endregion
export { page };
