import './style.css';

const recommendations = ({ data }) => {
  console.log(data);

  const elements = Object.entries(data).map(([key, value]) => (
    <div className="profile">
      <h2 style={{ textAlign: 'center' }}>User : {key}</h2>
      <table className='scoreTable'>
      <thead>
    <tr>
      <th>Score (50)</th>
      <th>Field</th>
      <th>Compatibility Points (7)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>{value[0][0]}</td>
      <td><h3>-------  Openness  -------</h3></td>
      <td>{value[1][0]}</td>
    </tr>
    <tr>
      <td>{value[0][1]}</td>
      <td><h3>--  Conscientiousness  --</h3></td>
      <td>{value[1][1]}</td>
    </tr>
    <tr>
      <td>{value[0][2]}</td>
      <td><h3>--  Extraversion  --</h3></td>
      <td>{value[1][2]}</td>
    </tr>
    <tr>
      <td>{value[0][3]}</td>
      <td><h3>--  Agreeableness  --</h3></td>
      <td>{value[1][3]}</td>
    </tr>
    <tr>
      <td>{value[0][4]}</td>
      <td><h3>--  Neuroticism  --</h3></td>
      <td>{value[1][4]}</td>
    </tr>
  </tbody>
</table>



    </div>
  ));
  return (
    <div>
      {elements}
    </div>
  );
};

export default recommendations;
