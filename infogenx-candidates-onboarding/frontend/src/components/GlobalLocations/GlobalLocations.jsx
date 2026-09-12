import "./GlobalLocations.css";
import {
  FaMapMarkerAlt,
  FaPhoneAlt,
  FaEnvelope,
} from "react-icons/fa";

function GlobalLocations() {
  const offices = [
    {
      id: 1,
      flag: "🇦🇺",
      title: "Australia Office",
      address:
        "207/17 View Street, Mount Gravatt East, Brisbane, Queensland, QLD 4122, Australia",
      phone: "+61 403 331 910",
      email: "contactus@infogenx.com",
    },
    {
      id: 2,
      flag: "🇮🇳",
      title: "India Office",
      address:
        "Spaces Olympia, 10th Floor, Citius A Block, Phase 1, Plot No.1, SIDCO Industrial Estate, Guindy, Chennai, Tamil Nadu 600032",
      phone: "+91 9787806366",
      email: "contactus@infogenx.com",
    },
  ];

  return (
    <section className="global-locations">

      <div className="global-bg-circle bg-one"></div>
      <div className="global-bg-circle bg-two"></div>
      <div className="global-bg-circle bg-three"></div>

      <div className="global-container">

        <div className="global-heading">

          <span className="global-badge">
            OUR OFFICES
          </span>

          <h2>
            Global Locations
          </h2>

          <p>
            Connect with our international teams.
            We are available across Australia and India
            to support every stage of your onboarding journey.
          </p>

        </div>

        <div className="office-grid">

          {offices.map((office) => (

            <div
              className="office-card"
              key={office.id}
            >

              <div className="office-card-glow"></div>

              <div className="office-header">

                <div className="office-flag">
                  {office.flag}
                </div>

                <div>

                  <h3>{office.title}</h3>

                </div>

              </div>

              <div className="office-body">

                <div className="office-row">

                  <div className="office-icon">
                    <FaMapMarkerAlt />
                  </div>

                  <p>{office.address}</p>

                </div>

                <div className="office-row">

                  <div className="office-icon">
                    <FaPhoneAlt />
                  </div>

                  <p>{office.phone}</p>

                </div>

                <div className="office-row">

                  <div className="office-icon">
                    <FaEnvelope />
                  </div>

                  <p>{office.email}</p>

                </div>

              </div>

            </div>

          ))}

        </div>

      </div>

    </section>
  );
}

export default GlobalLocations;