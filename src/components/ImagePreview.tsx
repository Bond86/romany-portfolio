import { useEffect, useRef, useState } from 'react';
import { X, Maximize2 } from 'lucide-react';
export default function ImagePreview({src,alt}:{src:string,alt:string}){
 const [open,setOpen]=useState(false);const ref=useRef<HTMLDialogElement>(null);
 useEffect(()=>{if(!open)return;ref.current?.showModal();const before=document.body.style.overflow;document.body.style.overflow='hidden';return()=>{document.body.style.overflow=before;};},[open]);
 return <><button className="case-image-button" onClick={()=>setOpen(true)} aria-label={`Enlarge ${alt}`}><img src={src} alt={alt} width="1280" height="720"/><span><Maximize2 size={18}/></span></button>{open&&<dialog className="image-modal" ref={ref} aria-label={alt} onCancel={()=>setOpen(false)} onClick={e=>{if(e.target===e.currentTarget)setOpen(false);}}><div className="modal-header"><span>{alt}</span><button aria-label="Close image" onClick={()=>setOpen(false)}><X/></button></div><img src={src} alt={alt}/></dialog>}</>;
}
