import{B as O,s as q,o as S,c as C,m as k,r as j,a as B,b as w,l as G,d as Pt,f as N,e as D,t as wt,F as Ct,g as Tt,n as Ot,N as dt,h as Q,S as V,i as X,j as Z,k as lt,p as jt,P as H,C as At,Q as It,q as tt,T as ut,R as st,v as Bt,u as zt,K as Vt,W as Lt,U as Et,w as ct,x as Dt,y as Nt,z as nt,A as z,D as bt,E as Ut,G as Mt,H as Ft,I as L,J as E,L as pt,M as et,_ as Rt}from"./index-CCrGvbnS.js";var Y={};function Wt(t="pui_id_"){return Object.hasOwn(Y,t)||(Y[t]=0),Y[t]++,`${t}${Y[t]}`}var Kt=`
    .p-card {
        background: dt('card.background');
        color: dt('card.color');
        box-shadow: dt('card.shadow');
        border-radius: dt('card.border.radius');
        display: flex;
        flex-direction: column;
    }

    .p-card-caption {
        display: flex;
        flex-direction: column;
        gap: dt('card.caption.gap');
    }

    .p-card-body {
        padding: dt('card.body.padding');
        display: flex;
        flex-direction: column;
        gap: dt('card.body.gap');
    }

    .p-card-title {
        font-size: dt('card.title.font.size');
        font-weight: dt('card.title.font.weight');
    }

    .p-card-subtitle {
        color: dt('card.subtitle.color');
    }
`,Ht={root:"p-card p-component",header:"p-card-header",body:"p-card-body",caption:"p-card-caption",title:"p-card-title",subtitle:"p-card-subtitle",content:"p-card-content",footer:"p-card-footer"},Yt=O.extend({name:"card",style:Kt,classes:Ht}),qt={name:"BaseCard",extends:q,style:Yt,provide:function(){return{$pcCard:this,$parentInstance:this}}},ot={name:"Card",extends:qt,inheritAttrs:!1};function Gt(t,n,e,o,a,r){return S(),C("div",k({class:t.cx("root")},t.ptmi("root")),[t.$slots.header?(S(),C("div",k({key:0,class:t.cx("header")},t.ptm("header")),[j(t.$slots,"header")],16)):B("",!0),w("div",k({class:t.cx("body")},t.ptm("body")),[t.$slots.title||t.$slots.subtitle?(S(),C("div",k({key:0,class:t.cx("caption")},t.ptm("caption")),[t.$slots.title?(S(),C("div",k({key:0,class:t.cx("title")},t.ptm("title")),[j(t.$slots,"title")],16)):B("",!0),t.$slots.subtitle?(S(),C("div",k({key:1,class:t.cx("subtitle")},t.ptm("subtitle")),[j(t.$slots,"subtitle")],16)):B("",!0)],16)):B("",!0),w("div",k({class:t.cx("content")},t.ptm("content")),[j(t.$slots,"content")],16),t.$slots.footer?(S(),C("div",k({key:1,class:t.cx("footer")},t.ptm("footer")),[j(t.$slots,"footer")],16)):B("",!0)],16)],16)}ot.render=Gt;var Jt=`
.p-icon {
    display: inline-block;
    vertical-align: baseline;
    flex-shrink: 0;
}

.p-icon-spin {
    -webkit-animation: p-icon-spin 2s infinite linear;
    animation: p-icon-spin 2s infinite linear;
}

@-webkit-keyframes p-icon-spin {
    0% {
        -webkit-transform: rotate(0deg);
        transform: rotate(0deg);
    }
    100% {
        -webkit-transform: rotate(359deg);
        transform: rotate(359deg);
    }
}

@keyframes p-icon-spin {
    0% {
        -webkit-transform: rotate(0deg);
        transform: rotate(0deg);
    }
    100% {
        -webkit-transform: rotate(359deg);
        transform: rotate(359deg);
    }
}
`,Qt=O.extend({name:"baseicon",css:Jt});function U(t){"@babel/helpers - typeof";return U=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(n){return typeof n}:function(n){return n&&typeof Symbol=="function"&&n.constructor===Symbol&&n!==Symbol.prototype?"symbol":typeof n},U(t)}function gt(t,n){var e=Object.keys(t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(t);n&&(o=o.filter(function(a){return Object.getOwnPropertyDescriptor(t,a).enumerable})),e.push.apply(e,o)}return e}function ht(t){for(var n=1;n<arguments.length;n++){var e=arguments[n]!=null?arguments[n]:{};n%2?gt(Object(e),!0).forEach(function(o){Xt(t,o,e[o])}):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(e)):gt(Object(e)).forEach(function(o){Object.defineProperty(t,o,Object.getOwnPropertyDescriptor(e,o))})}return t}function Xt(t,n,e){return(n=Zt(n))in t?Object.defineProperty(t,n,{value:e,enumerable:!0,configurable:!0,writable:!0}):t[n]=e,t}function Zt(t){var n=tn(t,"string");return U(n)=="symbol"?n:n+""}function tn(t,n){if(U(t)!="object"||!t)return t;var e=t[Symbol.toPrimitive];if(e!==void 0){var o=e.call(t,n);if(U(o)!="object")return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return(n==="string"?String:Number)(t)}var nn={name:"BaseIcon",extends:q,props:{label:{type:String,default:void 0},spin:{type:Boolean,default:!1}},style:Qt,provide:function(){return{$pcIcon:this,$parentInstance:this}},methods:{pti:function(){var n=G(this.label);return ht(ht({},!this.isUnstyled&&{class:["p-icon",{"p-icon-spin":this.spin}]}),{},{role:n?void 0:"img","aria-label":n?void 0:this.label,"aria-hidden":n})}}},$t={name:"SpinnerIcon",extends:nn};function en(t){return dn(t)||an(t)||rn(t)||on()}function on(){throw new TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function rn(t,n){if(t){if(typeof t=="string")return rt(t,n);var e={}.toString.call(t).slice(8,-1);return e==="Object"&&t.constructor&&(e=t.constructor.name),e==="Map"||e==="Set"?Array.from(t):e==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(e)?rt(t,n):void 0}}function an(t){if(typeof Symbol<"u"&&t[Symbol.iterator]!=null||t["@@iterator"]!=null)return Array.from(t)}function dn(t){if(Array.isArray(t))return rt(t)}function rt(t,n){(n==null||n>t.length)&&(n=t.length);for(var e=0,o=Array(n);e<n;e++)o[e]=t[e];return o}function ln(t,n,e,o,a,r){return S(),C("svg",k({width:"14",height:"14",viewBox:"0 0 14 14",fill:"none",xmlns:"http://www.w3.org/2000/svg"},t.pti()),en(n[0]||(n[0]=[w("path",{d:"M6.99701 14C5.85441 13.999 4.72939 13.7186 3.72012 13.1832C2.71084 12.6478 1.84795 11.8737 1.20673 10.9284C0.565504 9.98305 0.165424 8.89526 0.041387 7.75989C-0.0826496 6.62453 0.073125 5.47607 0.495122 4.4147C0.917119 3.35333 1.59252 2.4113 2.46241 1.67077C3.33229 0.930247 4.37024 0.413729 5.4857 0.166275C6.60117 -0.0811796 7.76026 -0.0520535 8.86188 0.251112C9.9635 0.554278 10.9742 1.12227 11.8057 1.90555C11.915 2.01493 11.9764 2.16319 11.9764 2.31778C11.9764 2.47236 11.915 2.62062 11.8057 2.73C11.7521 2.78503 11.688 2.82877 11.6171 2.85864C11.5463 2.8885 11.4702 2.90389 11.3933 2.90389C11.3165 2.90389 11.2404 2.8885 11.1695 2.85864C11.0987 2.82877 11.0346 2.78503 10.9809 2.73C9.9998 1.81273 8.73246 1.26138 7.39226 1.16876C6.05206 1.07615 4.72086 1.44794 3.62279 2.22152C2.52471 2.99511 1.72683 4.12325 1.36345 5.41602C1.00008 6.70879 1.09342 8.08723 1.62775 9.31926C2.16209 10.5513 3.10478 11.5617 4.29713 12.1803C5.48947 12.7989 6.85865 12.988 8.17414 12.7157C9.48963 12.4435 10.6711 11.7264 11.5196 10.6854C12.3681 9.64432 12.8319 8.34282 12.8328 7C12.8328 6.84529 12.8943 6.69692 13.0038 6.58752C13.1132 6.47812 13.2616 6.41667 13.4164 6.41667C13.5712 6.41667 13.7196 6.47812 13.8291 6.58752C13.9385 6.69692 14 6.84529 14 7C14 8.85651 13.2622 10.637 11.9489 11.9497C10.6356 13.2625 8.85432 14 6.99701 14Z",fill:"currentColor"},null,-1)])),16)}$t.render=ln;var un=`
    .p-badge {
        display: inline-flex;
        border-radius: dt('badge.border.radius');
        align-items: center;
        justify-content: center;
        padding: dt('badge.padding');
        background: dt('badge.primary.background');
        color: dt('badge.primary.color');
        font-size: dt('badge.font.size');
        font-weight: dt('badge.font.weight');
        min-width: dt('badge.min.width');
        height: dt('badge.height');
    }

    .p-badge-dot {
        width: dt('badge.dot.size');
        min-width: dt('badge.dot.size');
        height: dt('badge.dot.size');
        border-radius: 50%;
        padding: 0;
    }

    .p-badge-circle {
        padding: 0;
        border-radius: 50%;
    }

    .p-badge-secondary {
        background: dt('badge.secondary.background');
        color: dt('badge.secondary.color');
    }

    .p-badge-success {
        background: dt('badge.success.background');
        color: dt('badge.success.color');
    }

    .p-badge-info {
        background: dt('badge.info.background');
        color: dt('badge.info.color');
    }

    .p-badge-warn {
        background: dt('badge.warn.background');
        color: dt('badge.warn.color');
    }

    .p-badge-danger {
        background: dt('badge.danger.background');
        color: dt('badge.danger.color');
    }

    .p-badge-contrast {
        background: dt('badge.contrast.background');
        color: dt('badge.contrast.color');
    }

    .p-badge-sm {
        font-size: dt('badge.sm.font.size');
        min-width: dt('badge.sm.min.width');
        height: dt('badge.sm.height');
    }

    .p-badge-lg {
        font-size: dt('badge.lg.font.size');
        min-width: dt('badge.lg.min.width');
        height: dt('badge.lg.height');
    }

    .p-badge-xl {
        font-size: dt('badge.xl.font.size');
        min-width: dt('badge.xl.min.width');
        height: dt('badge.xl.height');
    }
`,sn={root:function(n){var e=n.props,o=n.instance;return["p-badge p-component",{"p-badge-circle":Pt(e.value)&&String(e.value).length===1,"p-badge-dot":G(e.value)&&!o.$slots.default,"p-badge-sm":e.size==="small","p-badge-lg":e.size==="large","p-badge-xl":e.size==="xlarge","p-badge-info":e.severity==="info","p-badge-success":e.severity==="success","p-badge-warn":e.severity==="warn","p-badge-danger":e.severity==="danger","p-badge-secondary":e.severity==="secondary","p-badge-contrast":e.severity==="contrast"}]}},cn=O.extend({name:"badge",style:un,classes:sn}),bn={name:"BaseBadge",extends:q,props:{value:{type:[String,Number],default:null},severity:{type:String,default:null},size:{type:String,default:null}},style:cn,provide:function(){return{$pcBadge:this,$parentInstance:this}}};function M(t){"@babel/helpers - typeof";return M=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(n){return typeof n}:function(n){return n&&typeof Symbol=="function"&&n.constructor===Symbol&&n!==Symbol.prototype?"symbol":typeof n},M(t)}function vt(t,n,e){return(n=pn(n))in t?Object.defineProperty(t,n,{value:e,enumerable:!0,configurable:!0,writable:!0}):t[n]=e,t}function pn(t){var n=gn(t,"string");return M(n)=="symbol"?n:n+""}function gn(t,n){if(M(t)!="object"||!t)return t;var e=t[Symbol.toPrimitive];if(e!==void 0){var o=e.call(t,n);if(M(o)!="object")return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return(n==="string"?String:Number)(t)}var St={name:"Badge",extends:bn,inheritAttrs:!1,computed:{dataP:function(){return N(vt(vt({circle:this.value!=null&&String(this.value).length===1,empty:this.value==null&&!this.$slots.default},this.severity,this.severity),this.size,this.size))}}},hn=["data-p"];function vn(t,n,e,o,a,r){return S(),C("span",k({class:t.cx("root"),"data-p":r.dataP},t.ptmi("root")),[j(t.$slots,"default",{},function(){return[D(wt(t.value),1)]})],16,hn)}St.render=vn;function F(t){"@babel/helpers - typeof";return F=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(n){return typeof n}:function(n){return n&&typeof Symbol=="function"&&n.constructor===Symbol&&n!==Symbol.prototype?"symbol":typeof n},F(t)}function ft(t,n){return kn(t)||yn(t,n)||mn(t,n)||fn()}function fn(){throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function mn(t,n){if(t){if(typeof t=="string")return mt(t,n);var e={}.toString.call(t).slice(8,-1);return e==="Object"&&t.constructor&&(e=t.constructor.name),e==="Map"||e==="Set"?Array.from(t):e==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(e)?mt(t,n):void 0}}function mt(t,n){(n==null||n>t.length)&&(n=t.length);for(var e=0,o=Array(n);e<n;e++)o[e]=t[e];return o}function yn(t,n){var e=t==null?null:typeof Symbol<"u"&&t[Symbol.iterator]||t["@@iterator"];if(e!=null){var o,a,r,c,d=[],i=!0,s=!1;try{if(r=(e=e.call(t)).next,n!==0)for(;!(i=(o=r.call(e)).done)&&(d.push(o.value),d.length!==n);i=!0);}catch(p){s=!0,a=p}finally{try{if(!i&&e.return!=null&&(c=e.return(),Object(c)!==c))return}finally{if(s)throw a}}return d}}function kn(t){if(Array.isArray(t))return t}function yt(t,n){var e=Object.keys(t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(t);n&&(o=o.filter(function(a){return Object.getOwnPropertyDescriptor(t,a).enumerable})),e.push.apply(e,o)}return e}function g(t){for(var n=1;n<arguments.length;n++){var e=arguments[n]!=null?arguments[n]:{};n%2?yt(Object(e),!0).forEach(function(o){at(t,o,e[o])}):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(e)):yt(Object(e)).forEach(function(o){Object.defineProperty(t,o,Object.getOwnPropertyDescriptor(e,o))})}return t}function at(t,n,e){return(n=wn(n))in t?Object.defineProperty(t,n,{value:e,enumerable:!0,configurable:!0,writable:!0}):t[n]=e,t}function wn(t){var n=$n(t,"string");return F(n)=="symbol"?n:n+""}function $n(t,n){if(F(t)!="object"||!t)return t;var e=t[Symbol.toPrimitive];if(e!==void 0){var o=e.call(t,n);if(F(o)!="object")return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return(n==="string"?String:Number)(t)}var b={_getMeta:function(){return[lt(arguments.length<=0?void 0:arguments[0])||arguments.length<=0?void 0:arguments[0],jt(lt(arguments.length<=0?void 0:arguments[0])?arguments.length<=0?void 0:arguments[0]:arguments.length<=1?void 0:arguments[1])]},_getConfig:function(n,e){var o,a,r;return(o=(n==null||(a=n.instance)===null||a===void 0?void 0:a.$primevue)||(e==null||(r=e.ctx)===null||r===void 0||(r=r.appContext)===null||r===void 0||(r=r.config)===null||r===void 0||(r=r.globalProperties)===null||r===void 0?void 0:r.$primevue))===null||o===void 0?void 0:o.config},_getOptionValue:Ct,_getPTValue:function(){var n,e,o=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},r=arguments.length>2&&arguments[2]!==void 0?arguments[2]:"",c=arguments.length>3&&arguments[3]!==void 0?arguments[3]:{},d=arguments.length>4&&arguments[4]!==void 0?arguments[4]:!0,i=function(){var T=b._getOptionValue.apply(b,arguments);return X(T)||At(T)?{class:T}:T},s=((n=o.binding)===null||n===void 0||(n=n.value)===null||n===void 0?void 0:n.ptOptions)||((e=o.$primevueConfig)===null||e===void 0?void 0:e.ptOptions)||{},p=s.mergeSections,l=p===void 0?!0:p,h=s.mergeProps,f=h===void 0?!1:h,m=d?b._useDefaultPT(o,o.defaultPT(),i,r,c):void 0,_=b._usePT(o,b._getPT(a,o.$name),i,r,g(g({},c),{},{global:m||{}})),y=b._getPTDatasets(o,r);return l||!l&&_?f?b._mergeProps(o,f,m,_,y):g(g(g({},m),_),y):g(g({},_),y)},_getPTDatasets:function(){var n=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:"",o="data-pc-";return g(g({},e==="root"&&at({},"".concat(o,"name"),Z(n.$name))),{},at({},"".concat(o,"section"),Z(e)))},_getPT:function(n){var e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:"",o=arguments.length>2?arguments[2]:void 0,a=function(c){var d,i=o?o(c):c,s=Z(e);return(d=i==null?void 0:i[s])!==null&&d!==void 0?d:i};return n&&Object.hasOwn(n,"_usept")?{_usept:n._usept,originalValue:a(n.originalValue),value:a(n.value)}:a(n)},_usePT:function(){var n=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},e=arguments.length>1?arguments[1]:void 0,o=arguments.length>2?arguments[2]:void 0,a=arguments.length>3?arguments[3]:void 0,r=arguments.length>4?arguments[4]:void 0,c=function(y){return o(y,a,r)};if(e&&Object.hasOwn(e,"_usept")){var d,i=e._usept||((d=n.$primevueConfig)===null||d===void 0?void 0:d.ptOptions)||{},s=i.mergeSections,p=s===void 0?!0:s,l=i.mergeProps,h=l===void 0?!1:l,f=c(e.originalValue),m=c(e.value);return f===void 0&&m===void 0?void 0:X(m)?m:X(f)?f:p||!p&&m?h?b._mergeProps(n,h,f,m):g(g({},f),m):m}return c(e)},_useDefaultPT:function(){var n=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},o=arguments.length>2?arguments[2]:void 0,a=arguments.length>3?arguments[3]:void 0,r=arguments.length>4?arguments[4]:void 0;return b._usePT(n,e,o,a,r)},_loadStyles:function(){var n,e=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},o=arguments.length>1?arguments[1]:void 0,a=arguments.length>2?arguments[2]:void 0,r=b._getConfig(o,a),c={nonce:r==null||(n=r.csp)===null||n===void 0?void 0:n.nonce};b._loadCoreStyles(e,c),b._loadThemeStyles(e,c),b._loadScopedThemeStyles(e,c),b._removeThemeListeners(e),e.$loadStyles=function(){return b._loadThemeStyles(e,c)},b._themeChangeListener(e.$loadStyles)},_loadCoreStyles:function(){var n,e,o=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},a=arguments.length>1?arguments[1]:void 0;if(!Q.isStyleNameLoaded((n=o.$style)===null||n===void 0?void 0:n.name)&&(e=o.$style)!==null&&e!==void 0&&e.name){var r;O.loadCSS(a),(r=o.$style)===null||r===void 0||r.loadCSS(a),Q.setLoadedStyleName(o.$style.name)}},_loadThemeStyles:function(){var n,e,o,a=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},r=arguments.length>1?arguments[1]:void 0;if(!(a!=null&&a.isUnstyled()||(a==null||(n=a.theme)===null||n===void 0?void 0:n.call(a))==="none")){if(!V.isStyleNameLoaded("common")){var c,d,i=((c=a.$style)===null||c===void 0||(d=c.getCommonTheme)===null||d===void 0?void 0:d.call(c))||{},s=i.primitive,p=i.semantic,l=i.global,h=i.style;O.load(s==null?void 0:s.css,g({name:"primitive-variables"},r)),O.load(p==null?void 0:p.css,g({name:"semantic-variables"},r)),O.load(l==null?void 0:l.css,g({name:"global-variables"},r)),O.loadStyle(g({name:"global-style"},r),h),V.setLoadedStyleName("common")}if(!V.isStyleNameLoaded((e=a.$style)===null||e===void 0?void 0:e.name)&&(o=a.$style)!==null&&o!==void 0&&o.name){var f,m,_,y,x=((f=a.$style)===null||f===void 0||(m=f.getDirectiveTheme)===null||m===void 0?void 0:m.call(f))||{},T=x.css,$=x.style;(_=a.$style)===null||_===void 0||_.load(T,g({name:"".concat(a.$style.name,"-variables")},r)),(y=a.$style)===null||y===void 0||y.loadStyle(g({name:"".concat(a.$style.name,"-style")},r),$),V.setLoadedStyleName(a.$style.name)}if(!V.isStyleNameLoaded("layer-order")){var u,v,I=(u=a.$style)===null||u===void 0||(v=u.getLayerOrderThemeCSS)===null||v===void 0?void 0:v.call(u);O.load(I,g({name:"layer-order",first:!0},r)),V.setLoadedStyleName("layer-order")}}},_loadScopedThemeStyles:function(){var n=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},e=arguments.length>1?arguments[1]:void 0,o=n.preset();if(o&&n.$attrSelector){var a,r,c,d=((a=n.$style)===null||a===void 0||(r=a.getPresetTheme)===null||r===void 0?void 0:r.call(a,o,"[".concat(n.$attrSelector,"]")))||{},i=d.css,s=(c=n.$style)===null||c===void 0?void 0:c.load(i,g({name:"".concat(n.$attrSelector,"-").concat(n.$style.name)},e));n.scopedStyleEl=s.el}},_themeChangeListener:function(){var n=arguments.length>0&&arguments[0]!==void 0?arguments[0]:function(){};Q.clearLoadedStyleNames(),dt.on("theme:change",n)},_removeThemeListeners:function(){var n=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};dt.off("theme:change",n.$loadStyles),n.$loadStyles=void 0},_hook:function(n,e,o,a,r,c){var d,i,s="on".concat(Ot(e)),p=b._getConfig(a,r),l=o==null?void 0:o.$instance,h=b._usePT(l,b._getPT(a==null||(d=a.value)===null||d===void 0?void 0:d.pt,n),b._getOptionValue,"hooks.".concat(s)),f=b._useDefaultPT(l,p==null||(i=p.pt)===null||i===void 0||(i=i.directives)===null||i===void 0?void 0:i[n],b._getOptionValue,"hooks.".concat(s)),m={el:o,binding:a,vnode:r,prevVnode:c};h==null||h(l,m),f==null||f(l,m)},_mergeProps:function(){for(var n=arguments.length>1?arguments[1]:void 0,e=arguments.length,o=new Array(e>2?e-2:0),a=2;a<e;a++)o[a-2]=arguments[a];return Tt(n)?n.apply(void 0,o):k.apply(void 0,o)},_extend:function(n){var e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},o=function(d,i,s,p,l){var h,f,m,_;i._$instances=i._$instances||{};var y=b._getConfig(s,p),x=i._$instances[n]||{},T=G(x)?g(g({},e),e==null?void 0:e.methods):{};i._$instances[n]=g(g({},x),{},{$name:n,$host:i,$binding:s,$modifiers:s==null?void 0:s.modifiers,$value:s==null?void 0:s.value,$el:x.$el||i||void 0,$style:g({classes:void 0,inlineStyles:void 0,load:function(){},loadCSS:function(){},loadStyle:function(){}},e==null?void 0:e.style),$primevueConfig:y,$attrSelector:(h=i.$pd)===null||h===void 0||(h=h[n])===null||h===void 0?void 0:h.attrSelector,defaultPT:function(){return b._getPT(y==null?void 0:y.pt,void 0,function(u){var v;return u==null||(v=u.directives)===null||v===void 0?void 0:v[n]})},isUnstyled:function(){var u,v;return((u=i._$instances[n])===null||u===void 0||(u=u.$binding)===null||u===void 0||(u=u.value)===null||u===void 0?void 0:u.unstyled)!==void 0?(v=i._$instances[n])===null||v===void 0||(v=v.$binding)===null||v===void 0||(v=v.value)===null||v===void 0?void 0:v.unstyled:y==null?void 0:y.unstyled},theme:function(){var u;return(u=i._$instances[n])===null||u===void 0||(u=u.$primevueConfig)===null||u===void 0?void 0:u.theme},preset:function(){var u;return(u=i._$instances[n])===null||u===void 0||(u=u.$binding)===null||u===void 0||(u=u.value)===null||u===void 0?void 0:u.dt},ptm:function(){var u,v=arguments.length>0&&arguments[0]!==void 0?arguments[0]:"",I=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{};return b._getPTValue(i._$instances[n],(u=i._$instances[n])===null||u===void 0||(u=u.$binding)===null||u===void 0||(u=u.value)===null||u===void 0?void 0:u.pt,v,g({},I))},ptmo:function(){var u=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},v=arguments.length>1&&arguments[1]!==void 0?arguments[1]:"",I=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{};return b._getPTValue(i._$instances[n],u,v,I,!1)},cx:function(){var u,v,I=arguments.length>0&&arguments[0]!==void 0?arguments[0]:"",J=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{};return(u=i._$instances[n])!==null&&u!==void 0&&u.isUnstyled()?void 0:b._getOptionValue((v=i._$instances[n])===null||v===void 0||(v=v.$style)===null||v===void 0?void 0:v.classes,I,g({},J))},sx:function(){var u,v=arguments.length>0&&arguments[0]!==void 0?arguments[0]:"",I=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!0,J=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{};return I?b._getOptionValue((u=i._$instances[n])===null||u===void 0||(u=u.$style)===null||u===void 0?void 0:u.inlineStyles,v,g({},J)):void 0}},T),i.$instance=i._$instances[n],(f=(m=i.$instance)[d])===null||f===void 0||f.call(m,i,s,p,l),i["$".concat(n)]=i.$instance,b._hook(n,d,i,s,p,l),i.$pd||(i.$pd={}),i.$pd[n]=g(g({},(_=i.$pd)===null||_===void 0?void 0:_[n]),{},{name:n,instance:i._$instances[n]})},a=function(d){var i,s,p,l=d._$instances[n],h=l==null?void 0:l.watch,f=function(y){var x,T=y.newValue,$=y.oldValue;return h==null||(x=h.config)===null||x===void 0?void 0:x.call(l,T,$)},m=function(y){var x,T=y.newValue,$=y.oldValue;return h==null||(x=h["config.ripple"])===null||x===void 0?void 0:x.call(l,T,$)};l.$watchersCallback={config:f,"config.ripple":m},h==null||(i=h.config)===null||i===void 0||i.call(l,l==null?void 0:l.$primevueConfig),H.on("config:change",f),h==null||(s=h["config.ripple"])===null||s===void 0||s.call(l,l==null||(p=l.$primevueConfig)===null||p===void 0?void 0:p.ripple),H.on("config:ripple:change",m)},r=function(d){var i=d._$instances[n].$watchersCallback;i&&(H.off("config:change",i.config),H.off("config:ripple:change",i["config.ripple"]),d._$instances[n].$watchersCallback=void 0)};return{created:function(d,i,s,p){d.$pd||(d.$pd={}),d.$pd[n]={name:n,attrSelector:Wt("pd")},o("created",d,i,s,p)},beforeMount:function(d,i,s,p){var l;b._loadStyles((l=d.$pd[n])===null||l===void 0?void 0:l.instance,i,s),o("beforeMount",d,i,s,p),a(d)},mounted:function(d,i,s,p){var l;b._loadStyles((l=d.$pd[n])===null||l===void 0?void 0:l.instance,i,s),o("mounted",d,i,s,p)},beforeUpdate:function(d,i,s,p){o("beforeUpdate",d,i,s,p)},updated:function(d,i,s,p){var l;b._loadStyles((l=d.$pd[n])===null||l===void 0?void 0:l.instance,i,s),o("updated",d,i,s,p)},beforeUnmount:function(d,i,s,p){var l;r(d),b._removeThemeListeners((l=d.$pd[n])===null||l===void 0?void 0:l.instance),o("beforeUnmount",d,i,s,p)},unmounted:function(d,i,s,p){var l;(l=d.$pd[n])===null||l===void 0||(l=l.instance)===null||l===void 0||(l=l.scopedStyleEl)===null||l===void 0||(l=l.value)===null||l===void 0||l.remove(),o("unmounted",d,i,s,p)}}},extend:function(){var n=b._getMeta.apply(b,arguments),e=ft(n,2),o=e[0],a=e[1];return g({extend:function(){var c=b._getMeta.apply(b,arguments),d=ft(c,2),i=d[0],s=d[1];return b.extend(i,g(g(g({},a),a==null?void 0:a.methods),s))}},b._extend(o,a))}},Sn=`
    .p-ink {
        display: block;
        position: absolute;
        background: dt('ripple.background');
        border-radius: 100%;
        transform: scale(0);
        pointer-events: none;
    }

    .p-ink-active {
        animation: ripple 0.4s linear;
    }

    @keyframes ripple {
        100% {
            opacity: 0;
            transform: scale(2.5);
        }
    }
`,_n={root:"p-ink"},xn=O.extend({name:"ripple-directive",style:Sn,classes:_n}),Pn=b.extend({style:xn});function R(t){"@babel/helpers - typeof";return R=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(n){return typeof n}:function(n){return n&&typeof Symbol=="function"&&n.constructor===Symbol&&n!==Symbol.prototype?"symbol":typeof n},R(t)}function Cn(t){return An(t)||jn(t)||On(t)||Tn()}function Tn(){throw new TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function On(t,n){if(t){if(typeof t=="string")return it(t,n);var e={}.toString.call(t).slice(8,-1);return e==="Object"&&t.constructor&&(e=t.constructor.name),e==="Map"||e==="Set"?Array.from(t):e==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(e)?it(t,n):void 0}}function jn(t){if(typeof Symbol<"u"&&t[Symbol.iterator]!=null||t["@@iterator"]!=null)return Array.from(t)}function An(t){if(Array.isArray(t))return it(t)}function it(t,n){(n==null||n>t.length)&&(n=t.length);for(var e=0,o=Array(n);e<n;e++)o[e]=t[e];return o}function kt(t,n,e){return(n=In(n))in t?Object.defineProperty(t,n,{value:e,enumerable:!0,configurable:!0,writable:!0}):t[n]=e,t}function In(t){var n=Bn(t,"string");return R(n)=="symbol"?n:n+""}function Bn(t,n){if(R(t)!="object"||!t)return t;var e=t[Symbol.toPrimitive];if(e!==void 0){var o=e.call(t,n);if(R(o)!="object")return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return(n==="string"?String:Number)(t)}var zn=Pn.extend("ripple",{watch:{"config.ripple":function(n){n?(this.createRipple(this.$host),this.bindEvents(this.$host),this.$host.setAttribute("data-pd-ripple",!0),this.$host.style.overflow="hidden",this.$host.style.position="relative"):(this.remove(this.$host),this.$host.removeAttribute("data-pd-ripple"))}},unmounted:function(n){this.remove(n)},timeout:void 0,methods:{bindEvents:function(n){n.addEventListener("mousedown",this.onMouseDown.bind(this))},unbindEvents:function(n){n.removeEventListener("mousedown",this.onMouseDown.bind(this))},createRipple:function(n){var e=this.getInk(n);e||(e=Et("span",kt(kt({role:"presentation","aria-hidden":!0,"data-p-ink":!0,"data-p-ink-active":!1,class:!this.isUnstyled()&&this.cx("root"),onAnimationEnd:this.onAnimationEnd.bind(this)},this.$attrSelector,""),"p-bind",this.ptm("root"))),n.appendChild(e),this.$el=e)},remove:function(n){var e=this.getInk(n);e&&(this.$host.style.overflow="",this.$host.style.position="",this.unbindEvents(n),e.removeEventListener("animationend",this.onAnimationEnd),e.remove())},onMouseDown:function(n){var e=this,o=n.currentTarget,a=this.getInk(o);if(!(!a||getComputedStyle(a,null).display==="none")){if(!this.isUnstyled()&&tt(a,"p-ink-active"),a.setAttribute("data-p-ink-active","false"),!ut(a)&&!st(a)){var r=Math.max(Bt(o),zt(o));a.style.height=r+"px",a.style.width=r+"px"}var c=Vt(o),d=n.pageX-c.left+document.body.scrollTop-st(a)/2,i=n.pageY-c.top+document.body.scrollLeft-ut(a)/2;a.style.top=i+"px",a.style.left=d+"px",!this.isUnstyled()&&Lt(a,"p-ink-active"),a.setAttribute("data-p-ink-active","true"),this.timeout=setTimeout(function(){a&&(!e.isUnstyled()&&tt(a,"p-ink-active"),a.setAttribute("data-p-ink-active","false"))},401)}},onAnimationEnd:function(n){this.timeout&&clearTimeout(this.timeout),!this.isUnstyled()&&tt(n.currentTarget,"p-ink-active"),n.currentTarget.setAttribute("data-p-ink-active","false")},getInk:function(n){return n&&n.children?Cn(n.children).find(function(e){return It(e,"data-pc-name")==="ripple"}):void 0}}}),Vn=`
    .p-button {
        display: inline-flex;
        cursor: pointer;
        user-select: none;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        position: relative;
        color: dt('button.primary.color');
        background: dt('button.primary.background');
        border: 1px solid dt('button.primary.border.color');
        padding: dt('button.padding.y') dt('button.padding.x');
        font-size: 1rem;
        font-family: inherit;
        font-feature-settings: inherit;
        transition:
            background dt('button.transition.duration'),
            color dt('button.transition.duration'),
            border-color dt('button.transition.duration'),
            outline-color dt('button.transition.duration'),
            box-shadow dt('button.transition.duration');
        border-radius: dt('button.border.radius');
        outline-color: transparent;
        gap: dt('button.gap');
    }

    .p-button:disabled {
        cursor: default;
    }

    .p-button-icon-right {
        order: 1;
    }

    .p-button-icon-right:dir(rtl) {
        order: -1;
    }

    .p-button:not(.p-button-vertical) .p-button-icon:not(.p-button-icon-right):dir(rtl) {
        order: 1;
    }

    .p-button-icon-bottom {
        order: 2;
    }

    .p-button-icon-only {
        width: dt('button.icon.only.width');
        padding-inline-start: 0;
        padding-inline-end: 0;
        gap: 0;
    }

    .p-button-icon-only.p-button-rounded {
        border-radius: 50%;
        height: dt('button.icon.only.width');
    }

    .p-button-icon-only .p-button-label {
        visibility: hidden;
        width: 0;
    }

    .p-button-icon-only::after {
        content: " ";
        visibility: hidden;
        width: 0;
    }

    .p-button-sm {
        font-size: dt('button.sm.font.size');
        padding: dt('button.sm.padding.y') dt('button.sm.padding.x');
    }

    .p-button-sm .p-button-icon {
        font-size: dt('button.sm.font.size');
    }

    .p-button-sm.p-button-icon-only {
        width: dt('button.sm.icon.only.width');
    }

    .p-button-sm.p-button-icon-only.p-button-rounded {
        height: dt('button.sm.icon.only.width');
    }

    .p-button-lg {
        font-size: dt('button.lg.font.size');
        padding: dt('button.lg.padding.y') dt('button.lg.padding.x');
    }

    .p-button-lg .p-button-icon {
        font-size: dt('button.lg.font.size');
    }

    .p-button-lg.p-button-icon-only {
        width: dt('button.lg.icon.only.width');
    }

    .p-button-lg.p-button-icon-only.p-button-rounded {
        height: dt('button.lg.icon.only.width');
    }

    .p-button-vertical {
        flex-direction: column;
    }

    .p-button-label {
        font-weight: dt('button.label.font.weight');
    }

    .p-button-fluid {
        width: 100%;
    }

    .p-button-fluid.p-button-icon-only {
        width: dt('button.icon.only.width');
    }

    .p-button:not(:disabled):hover {
        background: dt('button.primary.hover.background');
        border: 1px solid dt('button.primary.hover.border.color');
        color: dt('button.primary.hover.color');
    }

    .p-button:not(:disabled):active {
        background: dt('button.primary.active.background');
        border: 1px solid dt('button.primary.active.border.color');
        color: dt('button.primary.active.color');
    }

    .p-button:focus-visible {
        box-shadow: dt('button.primary.focus.ring.shadow');
        outline: dt('button.focus.ring.width') dt('button.focus.ring.style') dt('button.primary.focus.ring.color');
        outline-offset: dt('button.focus.ring.offset');
    }

    .p-button .p-badge {
        min-width: dt('button.badge.size');
        height: dt('button.badge.size');
        line-height: dt('button.badge.size');
    }

    .p-button-raised {
        box-shadow: dt('button.raised.shadow');
    }

    .p-button-rounded {
        border-radius: dt('button.rounded.border.radius');
    }

    .p-button-secondary {
        background: dt('button.secondary.background');
        border: 1px solid dt('button.secondary.border.color');
        color: dt('button.secondary.color');
    }

    .p-button-secondary:not(:disabled):hover {
        background: dt('button.secondary.hover.background');
        border: 1px solid dt('button.secondary.hover.border.color');
        color: dt('button.secondary.hover.color');
    }

    .p-button-secondary:not(:disabled):active {
        background: dt('button.secondary.active.background');
        border: 1px solid dt('button.secondary.active.border.color');
        color: dt('button.secondary.active.color');
    }

    .p-button-secondary:focus-visible {
        outline-color: dt('button.secondary.focus.ring.color');
        box-shadow: dt('button.secondary.focus.ring.shadow');
    }

    .p-button-success {
        background: dt('button.success.background');
        border: 1px solid dt('button.success.border.color');
        color: dt('button.success.color');
    }

    .p-button-success:not(:disabled):hover {
        background: dt('button.success.hover.background');
        border: 1px solid dt('button.success.hover.border.color');
        color: dt('button.success.hover.color');
    }

    .p-button-success:not(:disabled):active {
        background: dt('button.success.active.background');
        border: 1px solid dt('button.success.active.border.color');
        color: dt('button.success.active.color');
    }

    .p-button-success:focus-visible {
        outline-color: dt('button.success.focus.ring.color');
        box-shadow: dt('button.success.focus.ring.shadow');
    }

    .p-button-info {
        background: dt('button.info.background');
        border: 1px solid dt('button.info.border.color');
        color: dt('button.info.color');
    }

    .p-button-info:not(:disabled):hover {
        background: dt('button.info.hover.background');
        border: 1px solid dt('button.info.hover.border.color');
        color: dt('button.info.hover.color');
    }

    .p-button-info:not(:disabled):active {
        background: dt('button.info.active.background');
        border: 1px solid dt('button.info.active.border.color');
        color: dt('button.info.active.color');
    }

    .p-button-info:focus-visible {
        outline-color: dt('button.info.focus.ring.color');
        box-shadow: dt('button.info.focus.ring.shadow');
    }

    .p-button-warn {
        background: dt('button.warn.background');
        border: 1px solid dt('button.warn.border.color');
        color: dt('button.warn.color');
    }

    .p-button-warn:not(:disabled):hover {
        background: dt('button.warn.hover.background');
        border: 1px solid dt('button.warn.hover.border.color');
        color: dt('button.warn.hover.color');
    }

    .p-button-warn:not(:disabled):active {
        background: dt('button.warn.active.background');
        border: 1px solid dt('button.warn.active.border.color');
        color: dt('button.warn.active.color');
    }

    .p-button-warn:focus-visible {
        outline-color: dt('button.warn.focus.ring.color');
        box-shadow: dt('button.warn.focus.ring.shadow');
    }

    .p-button-help {
        background: dt('button.help.background');
        border: 1px solid dt('button.help.border.color');
        color: dt('button.help.color');
    }

    .p-button-help:not(:disabled):hover {
        background: dt('button.help.hover.background');
        border: 1px solid dt('button.help.hover.border.color');
        color: dt('button.help.hover.color');
    }

    .p-button-help:not(:disabled):active {
        background: dt('button.help.active.background');
        border: 1px solid dt('button.help.active.border.color');
        color: dt('button.help.active.color');
    }

    .p-button-help:focus-visible {
        outline-color: dt('button.help.focus.ring.color');
        box-shadow: dt('button.help.focus.ring.shadow');
    }

    .p-button-danger {
        background: dt('button.danger.background');
        border: 1px solid dt('button.danger.border.color');
        color: dt('button.danger.color');
    }

    .p-button-danger:not(:disabled):hover {
        background: dt('button.danger.hover.background');
        border: 1px solid dt('button.danger.hover.border.color');
        color: dt('button.danger.hover.color');
    }

    .p-button-danger:not(:disabled):active {
        background: dt('button.danger.active.background');
        border: 1px solid dt('button.danger.active.border.color');
        color: dt('button.danger.active.color');
    }

    .p-button-danger:focus-visible {
        outline-color: dt('button.danger.focus.ring.color');
        box-shadow: dt('button.danger.focus.ring.shadow');
    }

    .p-button-contrast {
        background: dt('button.contrast.background');
        border: 1px solid dt('button.contrast.border.color');
        color: dt('button.contrast.color');
    }

    .p-button-contrast:not(:disabled):hover {
        background: dt('button.contrast.hover.background');
        border: 1px solid dt('button.contrast.hover.border.color');
        color: dt('button.contrast.hover.color');
    }

    .p-button-contrast:not(:disabled):active {
        background: dt('button.contrast.active.background');
        border: 1px solid dt('button.contrast.active.border.color');
        color: dt('button.contrast.active.color');
    }

    .p-button-contrast:focus-visible {
        outline-color: dt('button.contrast.focus.ring.color');
        box-shadow: dt('button.contrast.focus.ring.shadow');
    }

    .p-button-outlined {
        background: transparent;
        border-color: dt('button.outlined.primary.border.color');
        color: dt('button.outlined.primary.color');
    }

    .p-button-outlined:not(:disabled):hover {
        background: dt('button.outlined.primary.hover.background');
        border-color: dt('button.outlined.primary.border.color');
        color: dt('button.outlined.primary.color');
    }

    .p-button-outlined:not(:disabled):active {
        background: dt('button.outlined.primary.active.background');
        border-color: dt('button.outlined.primary.border.color');
        color: dt('button.outlined.primary.color');
    }

    .p-button-outlined.p-button-secondary {
        border-color: dt('button.outlined.secondary.border.color');
        color: dt('button.outlined.secondary.color');
    }

    .p-button-outlined.p-button-secondary:not(:disabled):hover {
        background: dt('button.outlined.secondary.hover.background');
        border-color: dt('button.outlined.secondary.border.color');
        color: dt('button.outlined.secondary.color');
    }

    .p-button-outlined.p-button-secondary:not(:disabled):active {
        background: dt('button.outlined.secondary.active.background');
        border-color: dt('button.outlined.secondary.border.color');
        color: dt('button.outlined.secondary.color');
    }

    .p-button-outlined.p-button-success {
        border-color: dt('button.outlined.success.border.color');
        color: dt('button.outlined.success.color');
    }

    .p-button-outlined.p-button-success:not(:disabled):hover {
        background: dt('button.outlined.success.hover.background');
        border-color: dt('button.outlined.success.border.color');
        color: dt('button.outlined.success.color');
    }

    .p-button-outlined.p-button-success:not(:disabled):active {
        background: dt('button.outlined.success.active.background');
        border-color: dt('button.outlined.success.border.color');
        color: dt('button.outlined.success.color');
    }

    .p-button-outlined.p-button-info {
        border-color: dt('button.outlined.info.border.color');
        color: dt('button.outlined.info.color');
    }

    .p-button-outlined.p-button-info:not(:disabled):hover {
        background: dt('button.outlined.info.hover.background');
        border-color: dt('button.outlined.info.border.color');
        color: dt('button.outlined.info.color');
    }

    .p-button-outlined.p-button-info:not(:disabled):active {
        background: dt('button.outlined.info.active.background');
        border-color: dt('button.outlined.info.border.color');
        color: dt('button.outlined.info.color');
    }

    .p-button-outlined.p-button-warn {
        border-color: dt('button.outlined.warn.border.color');
        color: dt('button.outlined.warn.color');
    }

    .p-button-outlined.p-button-warn:not(:disabled):hover {
        background: dt('button.outlined.warn.hover.background');
        border-color: dt('button.outlined.warn.border.color');
        color: dt('button.outlined.warn.color');
    }

    .p-button-outlined.p-button-warn:not(:disabled):active {
        background: dt('button.outlined.warn.active.background');
        border-color: dt('button.outlined.warn.border.color');
        color: dt('button.outlined.warn.color');
    }

    .p-button-outlined.p-button-help {
        border-color: dt('button.outlined.help.border.color');
        color: dt('button.outlined.help.color');
    }

    .p-button-outlined.p-button-help:not(:disabled):hover {
        background: dt('button.outlined.help.hover.background');
        border-color: dt('button.outlined.help.border.color');
        color: dt('button.outlined.help.color');
    }

    .p-button-outlined.p-button-help:not(:disabled):active {
        background: dt('button.outlined.help.active.background');
        border-color: dt('button.outlined.help.border.color');
        color: dt('button.outlined.help.color');
    }

    .p-button-outlined.p-button-danger {
        border-color: dt('button.outlined.danger.border.color');
        color: dt('button.outlined.danger.color');
    }

    .p-button-outlined.p-button-danger:not(:disabled):hover {
        background: dt('button.outlined.danger.hover.background');
        border-color: dt('button.outlined.danger.border.color');
        color: dt('button.outlined.danger.color');
    }

    .p-button-outlined.p-button-danger:not(:disabled):active {
        background: dt('button.outlined.danger.active.background');
        border-color: dt('button.outlined.danger.border.color');
        color: dt('button.outlined.danger.color');
    }

    .p-button-outlined.p-button-contrast {
        border-color: dt('button.outlined.contrast.border.color');
        color: dt('button.outlined.contrast.color');
    }

    .p-button-outlined.p-button-contrast:not(:disabled):hover {
        background: dt('button.outlined.contrast.hover.background');
        border-color: dt('button.outlined.contrast.border.color');
        color: dt('button.outlined.contrast.color');
    }

    .p-button-outlined.p-button-contrast:not(:disabled):active {
        background: dt('button.outlined.contrast.active.background');
        border-color: dt('button.outlined.contrast.border.color');
        color: dt('button.outlined.contrast.color');
    }

    .p-button-outlined.p-button-plain {
        border-color: dt('button.outlined.plain.border.color');
        color: dt('button.outlined.plain.color');
    }

    .p-button-outlined.p-button-plain:not(:disabled):hover {
        background: dt('button.outlined.plain.hover.background');
        border-color: dt('button.outlined.plain.border.color');
        color: dt('button.outlined.plain.color');
    }

    .p-button-outlined.p-button-plain:not(:disabled):active {
        background: dt('button.outlined.plain.active.background');
        border-color: dt('button.outlined.plain.border.color');
        color: dt('button.outlined.plain.color');
    }

    .p-button-text {
        background: transparent;
        border-color: transparent;
        color: dt('button.text.primary.color');
    }

    .p-button-text:not(:disabled):hover {
        background: dt('button.text.primary.hover.background');
        border-color: transparent;
        color: dt('button.text.primary.color');
    }

    .p-button-text:not(:disabled):active {
        background: dt('button.text.primary.active.background');
        border-color: transparent;
        color: dt('button.text.primary.color');
    }

    .p-button-text.p-button-secondary {
        background: transparent;
        border-color: transparent;
        color: dt('button.text.secondary.color');
    }

    .p-button-text.p-button-secondary:not(:disabled):hover {
        background: dt('button.text.secondary.hover.background');
        border-color: transparent;
        color: dt('button.text.secondary.color');
    }

    .p-button-text.p-button-secondary:not(:disabled):active {
        background: dt('button.text.secondary.active.background');
        border-color: transparent;
        color: dt('button.text.secondary.color');
    }

    .p-button-text.p-button-success {
        background: transparent;
        border-color: transparent;
        color: dt('button.text.success.color');
    }

    .p-button-text.p-button-success:not(:disabled):hover {
        background: dt('button.text.success.hover.background');
        border-color: transparent;
        color: dt('button.text.success.color');
    }

    .p-button-text.p-button-success:not(:disabled):active {
        background: dt('button.text.success.active.background');
        border-color: transparent;
        color: dt('button.text.success.color');
    }

    .p-button-text.p-button-info {
        background: transparent;
        border-color: transparent;
        color: dt('button.text.info.color');
    }

    .p-button-text.p-button-info:not(:disabled):hover {
        background: dt('button.text.info.hover.background');
        border-color: transparent;
        color: dt('button.text.info.color');
    }

    .p-button-text.p-button-info:not(:disabled):active {
        background: dt('button.text.info.active.background');
        border-color: transparent;
        color: dt('button.text.info.color');
    }

    .p-button-text.p-button-warn {
        background: transparent;
        border-color: transparent;
        color: dt('button.text.warn.color');
    }

    .p-button-text.p-button-warn:not(:disabled):hover {
        background: dt('button.text.warn.hover.background');
        border-color: transparent;
        color: dt('button.text.warn.color');
    }

    .p-button-text.p-button-warn:not(:disabled):active {
        background: dt('button.text.warn.active.background');
        border-color: transparent;
        color: dt('button.text.warn.color');
    }

    .p-button-text.p-button-help {
        background: transparent;
        border-color: transparent;
        color: dt('button.text.help.color');
    }

    .p-button-text.p-button-help:not(:disabled):hover {
        background: dt('button.text.help.hover.background');
        border-color: transparent;
        color: dt('button.text.help.color');
    }

    .p-button-text.p-button-help:not(:disabled):active {
        background: dt('button.text.help.active.background');
        border-color: transparent;
        color: dt('button.text.help.color');
    }

    .p-button-text.p-button-danger {
        background: transparent;
        border-color: transparent;
        color: dt('button.text.danger.color');
    }

    .p-button-text.p-button-danger:not(:disabled):hover {
        background: dt('button.text.danger.hover.background');
        border-color: transparent;
        color: dt('button.text.danger.color');
    }

    .p-button-text.p-button-danger:not(:disabled):active {
        background: dt('button.text.danger.active.background');
        border-color: transparent;
        color: dt('button.text.danger.color');
    }

    .p-button-text.p-button-contrast {
        background: transparent;
        border-color: transparent;
        color: dt('button.text.contrast.color');
    }

    .p-button-text.p-button-contrast:not(:disabled):hover {
        background: dt('button.text.contrast.hover.background');
        border-color: transparent;
        color: dt('button.text.contrast.color');
    }

    .p-button-text.p-button-contrast:not(:disabled):active {
        background: dt('button.text.contrast.active.background');
        border-color: transparent;
        color: dt('button.text.contrast.color');
    }

    .p-button-text.p-button-plain {
        background: transparent;
        border-color: transparent;
        color: dt('button.text.plain.color');
    }

    .p-button-text.p-button-plain:not(:disabled):hover {
        background: dt('button.text.plain.hover.background');
        border-color: transparent;
        color: dt('button.text.plain.color');
    }

    .p-button-text.p-button-plain:not(:disabled):active {
        background: dt('button.text.plain.active.background');
        border-color: transparent;
        color: dt('button.text.plain.color');
    }

    .p-button-link {
        background: transparent;
        border-color: transparent;
        color: dt('button.link.color');
    }

    .p-button-link:not(:disabled):hover {
        background: transparent;
        border-color: transparent;
        color: dt('button.link.hover.color');
    }

    .p-button-link:not(:disabled):hover .p-button-label {
        text-decoration: underline;
    }

    .p-button-link:not(:disabled):active {
        background: transparent;
        border-color: transparent;
        color: dt('button.link.active.color');
    }
`;function W(t){"@babel/helpers - typeof";return W=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(n){return typeof n}:function(n){return n&&typeof Symbol=="function"&&n.constructor===Symbol&&n!==Symbol.prototype?"symbol":typeof n},W(t)}function A(t,n,e){return(n=Ln(n))in t?Object.defineProperty(t,n,{value:e,enumerable:!0,configurable:!0,writable:!0}):t[n]=e,t}function Ln(t){var n=En(t,"string");return W(n)=="symbol"?n:n+""}function En(t,n){if(W(t)!="object"||!t)return t;var e=t[Symbol.toPrimitive];if(e!==void 0){var o=e.call(t,n);if(W(o)!="object")return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return(n==="string"?String:Number)(t)}var Dn={root:function(n){var e=n.instance,o=n.props;return["p-button p-component",A(A(A(A(A(A(A(A(A({"p-button-icon-only":e.hasIcon&&!o.label&&!o.badge,"p-button-vertical":(o.iconPos==="top"||o.iconPos==="bottom")&&o.label,"p-button-loading":o.loading,"p-button-link":o.link||o.variant==="link"},"p-button-".concat(o.severity),o.severity),"p-button-raised",o.raised),"p-button-rounded",o.rounded),"p-button-text",o.text||o.variant==="text"),"p-button-outlined",o.outlined||o.variant==="outlined"),"p-button-sm",o.size==="small"),"p-button-lg",o.size==="large"),"p-button-plain",o.plain),"p-button-fluid",e.hasFluid)]},loadingIcon:"p-button-loading-icon",icon:function(n){var e=n.props;return["p-button-icon",A({},"p-button-icon-".concat(e.iconPos),e.label)]},label:"p-button-label"},Nn=O.extend({name:"button",style:Vn,classes:Dn}),Un={name:"BaseButton",extends:q,props:{label:{type:String,default:null},icon:{type:String,default:null},iconPos:{type:String,default:"left"},iconClass:{type:[String,Object],default:null},badge:{type:String,default:null},badgeClass:{type:[String,Object],default:null},badgeSeverity:{type:String,default:"secondary"},loading:{type:Boolean,default:!1},loadingIcon:{type:String,default:void 0},as:{type:[String,Object],default:"BUTTON"},asChild:{type:Boolean,default:!1},link:{type:Boolean,default:!1},severity:{type:String,default:null},raised:{type:Boolean,default:!1},rounded:{type:Boolean,default:!1},text:{type:Boolean,default:!1},outlined:{type:Boolean,default:!1},size:{type:String,default:null},variant:{type:String,default:null},plain:{type:Boolean,default:!1},fluid:{type:Boolean,default:null}},style:Nn,provide:function(){return{$pcButton:this,$parentInstance:this}}};function K(t){"@babel/helpers - typeof";return K=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(n){return typeof n}:function(n){return n&&typeof Symbol=="function"&&n.constructor===Symbol&&n!==Symbol.prototype?"symbol":typeof n},K(t)}function P(t,n,e){return(n=Mn(n))in t?Object.defineProperty(t,n,{value:e,enumerable:!0,configurable:!0,writable:!0}):t[n]=e,t}function Mn(t){var n=Fn(t,"string");return K(n)=="symbol"?n:n+""}function Fn(t,n){if(K(t)!="object"||!t)return t;var e=t[Symbol.toPrimitive];if(e!==void 0){var o=e.call(t,n);if(K(o)!="object")return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return(n==="string"?String:Number)(t)}var _t={name:"Button",extends:Un,inheritAttrs:!1,inject:{$pcFluid:{default:null}},methods:{getPTOptions:function(n){var e=n==="root"?this.ptmi:this.ptm;return e(n,{context:{disabled:this.disabled}})}},computed:{disabled:function(){return this.$attrs.disabled||this.$attrs.disabled===""||this.loading},defaultAriaLabel:function(){return this.label?this.label+(this.badge?" "+this.badge:""):this.$attrs.ariaLabel},hasIcon:function(){return this.icon||this.$slots.icon},attrs:function(){return k(this.asAttrs,this.a11yAttrs,this.getPTOptions("root"))},asAttrs:function(){return this.as==="BUTTON"?{type:"button",disabled:this.disabled}:void 0},a11yAttrs:function(){return{"aria-label":this.defaultAriaLabel,"data-pc-name":"button","data-p-disabled":this.disabled,"data-p-severity":this.severity}},hasFluid:function(){return G(this.fluid)?!!this.$pcFluid:this.fluid},dataP:function(){return N(P(P(P(P(P(P(P(P(P(P({},this.size,this.size),"icon-only",this.hasIcon&&!this.label&&!this.badge),"loading",this.loading),"fluid",this.hasFluid),"rounded",this.rounded),"raised",this.raised),"outlined",this.outlined||this.variant==="outlined"),"text",this.text||this.variant==="text"),"link",this.link||this.variant==="link"),"vertical",(this.iconPos==="top"||this.iconPos==="bottom")&&this.label))},dataIconP:function(){return N(P(P({},this.iconPos,this.iconPos),this.size,this.size))},dataLabelP:function(){return N(P(P({},this.size,this.size),"icon-only",this.hasIcon&&!this.label&&!this.badge))}},components:{SpinnerIcon:$t,Badge:St},directives:{ripple:zn}},Rn=["data-p"],Wn=["data-p"];function Kn(t,n,e,o,a,r){var c=ct("SpinnerIcon"),d=ct("Badge"),i=Dt("ripple");return t.asChild?j(t.$slots,"default",{key:1,class:bt(t.cx("root")),a11yAttrs:r.a11yAttrs}):Nt((S(),nt(Ut(t.as),k({key:0,class:t.cx("root"),"data-p":r.dataP},r.attrs),{default:z(function(){return[j(t.$slots,"default",{},function(){return[t.loading?j(t.$slots,"loadingicon",k({key:0,class:[t.cx("loadingIcon"),t.cx("icon")]},t.ptm("loadingIcon")),function(){return[t.loadingIcon?(S(),C("span",k({key:0,class:[t.cx("loadingIcon"),t.cx("icon"),t.loadingIcon]},t.ptm("loadingIcon")),null,16)):(S(),nt(c,k({key:1,class:[t.cx("loadingIcon"),t.cx("icon")],spin:""},t.ptm("loadingIcon")),null,16,["class"]))]}):j(t.$slots,"icon",k({key:1,class:[t.cx("icon")]},t.ptm("icon")),function(){return[t.icon?(S(),C("span",k({key:0,class:[t.cx("icon"),t.icon,t.iconClass],"data-p":r.dataIconP},t.ptm("icon")),null,16,Rn)):B("",!0)]}),t.label?(S(),C("span",k({key:2,class:t.cx("label")},t.ptm("label"),{"data-p":r.dataLabelP}),wt(t.label),17,Wn)):B("",!0),t.badge?(S(),nt(d,{key:3,value:t.badge,class:bt(t.badgeClass),severity:t.badgeSeverity,unstyled:t.unstyled,pt:t.ptm("pcBadge")},null,8,["value","class","severity","unstyled","pt"])):B("",!0)]})]}),_:3},16,["class","data-p"])),[[i]])}_t.render=Kn;var Hn=`
    .p-toggleswitch {
        display: inline-block;
        width: dt('toggleswitch.width');
        height: dt('toggleswitch.height');
    }

    .p-toggleswitch-input {
        cursor: pointer;
        appearance: none;
        position: absolute;
        top: 0;
        inset-inline-start: 0;
        width: 100%;
        height: 100%;
        padding: 0;
        margin: 0;
        opacity: 0;
        z-index: 1;
        outline: 0 none;
        border-radius: dt('toggleswitch.border.radius');
    }

    .p-toggleswitch-slider {
        cursor: pointer;
        width: 100%;
        height: 100%;
        border-width: dt('toggleswitch.border.width');
        border-style: solid;
        border-color: dt('toggleswitch.border.color');
        background: dt('toggleswitch.background');
        transition:
            background dt('toggleswitch.transition.duration'),
            color dt('toggleswitch.transition.duration'),
            border-color dt('toggleswitch.transition.duration'),
            outline-color dt('toggleswitch.transition.duration'),
            box-shadow dt('toggleswitch.transition.duration');
        border-radius: dt('toggleswitch.border.radius');
        outline-color: transparent;
        box-shadow: dt('toggleswitch.shadow');
    }

    .p-toggleswitch-handle {
        position: absolute;
        top: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        background: dt('toggleswitch.handle.background');
        color: dt('toggleswitch.handle.color');
        width: dt('toggleswitch.handle.size');
        height: dt('toggleswitch.handle.size');
        inset-inline-start: dt('toggleswitch.gap');
        margin-block-start: calc(-1 * calc(dt('toggleswitch.handle.size') / 2));
        border-radius: dt('toggleswitch.handle.border.radius');
        transition:
            background dt('toggleswitch.transition.duration'),
            color dt('toggleswitch.transition.duration'),
            inset-inline-start dt('toggleswitch.slide.duration'),
            box-shadow dt('toggleswitch.slide.duration');
    }

    .p-toggleswitch.p-toggleswitch-checked .p-toggleswitch-slider {
        background: dt('toggleswitch.checked.background');
        border-color: dt('toggleswitch.checked.border.color');
    }

    .p-toggleswitch.p-toggleswitch-checked .p-toggleswitch-handle {
        background: dt('toggleswitch.handle.checked.background');
        color: dt('toggleswitch.handle.checked.color');
        inset-inline-start: calc(dt('toggleswitch.width') - calc(dt('toggleswitch.handle.size') + dt('toggleswitch.gap')));
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:hover) .p-toggleswitch-slider {
        background: dt('toggleswitch.hover.background');
        border-color: dt('toggleswitch.hover.border.color');
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:hover) .p-toggleswitch-handle {
        background: dt('toggleswitch.handle.hover.background');
        color: dt('toggleswitch.handle.hover.color');
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:hover).p-toggleswitch-checked .p-toggleswitch-slider {
        background: dt('toggleswitch.checked.hover.background');
        border-color: dt('toggleswitch.checked.hover.border.color');
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:hover).p-toggleswitch-checked .p-toggleswitch-handle {
        background: dt('toggleswitch.handle.checked.hover.background');
        color: dt('toggleswitch.handle.checked.hover.color');
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:focus-visible) .p-toggleswitch-slider {
        box-shadow: dt('toggleswitch.focus.ring.shadow');
        outline: dt('toggleswitch.focus.ring.width') dt('toggleswitch.focus.ring.style') dt('toggleswitch.focus.ring.color');
        outline-offset: dt('toggleswitch.focus.ring.offset');
    }

    .p-toggleswitch.p-invalid > .p-toggleswitch-slider {
        border-color: dt('toggleswitch.invalid.border.color');
    }

    .p-toggleswitch.p-disabled {
        opacity: 1;
    }

    .p-toggleswitch.p-disabled .p-toggleswitch-slider {
        background: dt('toggleswitch.disabled.background');
    }

    .p-toggleswitch.p-disabled .p-toggleswitch-handle {
        background: dt('toggleswitch.handle.disabled.background');
    }
`,Yn={root:{position:"relative"}},qn={root:function(n){var e=n.instance,o=n.props;return["p-toggleswitch p-component",{"p-toggleswitch-checked":e.checked,"p-disabled":o.disabled,"p-invalid":e.$invalid}]},input:"p-toggleswitch-input",slider:"p-toggleswitch-slider",handle:"p-toggleswitch-handle"},Gn=O.extend({name:"toggleswitch",style:Hn,classes:qn,inlineStyles:Yn}),Jn={name:"BaseToggleSwitch",extends:Mt,props:{trueValue:{type:null,default:!0},falseValue:{type:null,default:!1},readonly:{type:Boolean,default:!1},tabindex:{type:Number,default:null},inputId:{type:String,default:null},inputClass:{type:[String,Object],default:null},inputStyle:{type:Object,default:null},ariaLabelledby:{type:String,default:null},ariaLabel:{type:String,default:null}},style:Gn,provide:function(){return{$pcToggleSwitch:this,$parentInstance:this}}},xt={name:"ToggleSwitch",extends:Jn,inheritAttrs:!1,emits:["change","focus","blur"],methods:{getPTOptions:function(n){var e=n==="root"?this.ptmi:this.ptm;return e(n,{context:{checked:this.checked,disabled:this.disabled}})},onChange:function(n){if(!this.disabled&&!this.readonly){var e=this.checked?this.falseValue:this.trueValue;this.writeValue(e,n),this.$emit("change",n)}},onFocus:function(n){this.$emit("focus",n)},onBlur:function(n){var e,o;this.$emit("blur",n),(e=(o=this.formField).onBlur)===null||e===void 0||e.call(o,n)}},computed:{checked:function(){return this.d_value===this.trueValue},dataP:function(){return N({checked:this.checked,disabled:this.disabled,invalid:this.$invalid})}}},Qn=["data-p-checked","data-p-disabled","data-p"],Xn=["id","checked","tabindex","disabled","readonly","aria-checked","aria-labelledby","aria-label","aria-invalid"],Zn=["data-p"],te=["data-p"];function ne(t,n,e,o,a,r){return S(),C("div",k({class:t.cx("root"),style:t.sx("root")},r.getPTOptions("root"),{"data-p-checked":r.checked,"data-p-disabled":t.disabled,"data-p":r.dataP}),[w("input",k({id:t.inputId,type:"checkbox",role:"switch",class:[t.cx("input"),t.inputClass],style:t.inputStyle,checked:r.checked,tabindex:t.tabindex,disabled:t.disabled,readonly:t.readonly,"aria-checked":r.checked,"aria-labelledby":t.ariaLabelledby,"aria-label":t.ariaLabel,"aria-invalid":t.invalid||void 0,onFocus:n[0]||(n[0]=function(){return r.onFocus&&r.onFocus.apply(r,arguments)}),onBlur:n[1]||(n[1]=function(){return r.onBlur&&r.onBlur.apply(r,arguments)}),onChange:n[2]||(n[2]=function(){return r.onChange&&r.onChange.apply(r,arguments)})},r.getPTOptions("input")),null,16,Xn),w("div",k({class:t.cx("slider")},r.getPTOptions("slider"),{"data-p":r.dataP}),[w("div",k({class:t.cx("handle")},r.getPTOptions("handle"),{"data-p":r.dataP}),[j(t.$slots,"handle",{checked:r.checked})],16,te)],16,Zn)],16,Qn)}xt.render=ne;const ee={class:"settings"},oe={class:"settings__cards"},re={class:"settings__fields"},ae={class:"settings__field"},ie={class:"settings__field"},de={class:"settings__toggle-row settings__toggle-row--desktop"},le={class:"settings__save"},ue=Ft({__name:"SettingsView",setup(t){const n=et("Alex Rivera"),e=et("alex@example.com"),o=et(!0);return(a,r)=>(S(),C("section",ee,[r[11]||(r[11]=w("header",{class:"settings__header"},[w("h1",{class:"settings__title"},"Settings"),w("p",{class:"settings__subtitle settings__subtitle--desktop"}," Manage your profile and how we reach you. "),w("p",{class:"settings__subtitle settings__subtitle--mobile"},"Profile and notifications")],-1)),w("div",oe,[L(E(ot),{class:"settings__card"},{title:z(()=>[...r[3]||(r[3]=[D("Profile",-1)])]),subtitle:z(()=>[...r[4]||(r[4]=[D("Your name and sign-in email.",-1)])]),content:z(()=>[w("div",re,[w("label",ae,[r[5]||(r[5]=w("span",{class:"settings__label"},"Display name",-1)),L(E(pt),{modelValue:n.value,"onUpdate:modelValue":r[0]||(r[0]=c=>n.value=c),class:"settings__input"},null,8,["modelValue"])]),w("label",ie,[r[6]||(r[6]=w("span",{class:"settings__label"},"Email",-1)),L(E(pt),{modelValue:e.value,"onUpdate:modelValue":r[1]||(r[1]=c=>e.value=c),type:"email",class:"settings__input"},null,8,["modelValue"])])])]),_:1}),L(E(ot),{class:"settings__card"},{title:z(()=>[...r[7]||(r[7]=[D("Notifications",-1)])]),subtitle:z(()=>[...r[8]||(r[8]=[D("Choose how you hear about account activity.",-1)])]),content:z(()=>[w("div",de,[r[9]||(r[9]=w("span",{class:"settings__toggle-label"},"Email updates",-1)),L(E(xt),{modelValue:o.value,"onUpdate:modelValue":r[2]||(r[2]=c=>o.value=c)},null,8,["modelValue"])]),r[10]||(r[10]=w("div",{class:"settings__empty settings__empty--mobile"},[w("p",{class:"settings__empty-title"},"No channels configured"),w("p",{class:"settings__empty-hint"},"Add email or push when you connect integrations.")],-1))]),_:1})]),w("div",le,[L(E(_t),{label:"Save changes"})])]))}}),ce=Rt(ue,[["__scopeId","data-v-bfed7c8d"]]);export{ce as default};
