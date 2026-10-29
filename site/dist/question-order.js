// Shuffle only on an explicit click; filtering and navigation reuse that order.
export class QuestionOrder {
  constructor() { this.mode='newest'; this.ids=[]; }
  byDate() { this.mode='newest'; }
  shuffle(questions, random=Math.random) {
    this.ids=questions.map(q=>q.id);
    for(let i=this.ids.length-1;i>0;i--){
      const j=Math.floor(random()*(i+1));
      [this.ids[i],this.ids[j]]=[this.ids[j],this.ids[i]];
    }
    this.mode='shuffle';
  }
  order(questions) {
    const rank=new Map(this.ids.map((id,i)=>[id,i]));
    return [...questions].sort((a,b)=>
      (this.mode==='shuffle'?(rank.get(a.id)??Infinity)-(rank.get(b.id)??Infinity):0)
      ||b.date.localeCompare(a.date)||a.id.localeCompare(b.id));
  }
  snapshot() { return {mode:this.mode,ids:this.mode==='shuffle'?[...this.ids]:[]}; }
  restore(value) {
    if(!value||!['newest','shuffle'].includes(value.mode)||!Array.isArray(value.ids))return;
    this.mode=value.mode;this.ids=[...new Set(value.ids.filter(id=>typeof id==='string'))];
  }
}
