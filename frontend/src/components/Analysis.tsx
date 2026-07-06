import { ASSET_BASE, type FiguresDoc } from "../api";

interface Props {
  figures: FiguresDoc;
}

export function Analysis({ figures }: Props) {
  return (
    <section className="section" id="charts">
      <div className="shell">
        <div className="sec-intro">
          <span className="eyebrow">The charts</span>
          <h2 className="sec-title">Which symptoms signal diabetes</h2>
          <p className="sec-lede">
            Made in Python with matplotlib and seaborn. They show how strongly each symptom is
            tied to a diagnosis, and what the {figures.model_name} model pays most attention to.
          </p>
        </div>

        <div className="gallery">
          {figures.figures.map((fig) => (
            <figure key={fig.file} className="card fig">
              <figcaption className="fig__cap">
                <span className="fig__title">{fig.title}</span>
                <span className="fig__note">{fig.caption}</span>
              </figcaption>
              <div className="fig__img-wrap">
                <img
                  className="fig__img"
                  src={`${ASSET_BASE}analysis/${fig.file}`}
                  alt={fig.title}
                  loading="lazy"
                />
              </div>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}
