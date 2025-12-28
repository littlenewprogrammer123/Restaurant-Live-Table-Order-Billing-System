import { useEffect, useState } from "react";
import api from "../api";
import Layout from "../components/Layout";

const statusColors = {
  AVAILABLE: "green",
  OCCUPIED: "orange",
  BILL_REQUESTED: "red",
  CLOSED: "gray",
};

function Tables() {
  const [tables, setTables] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchTables = async () => {
    try {
      const res = await api.get("tables/");
      setTables(res.data);
    } catch (err) {
      console.error("Failed to fetch tables", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTables();
  }, []);

  if (loading) return <div>Loading tables...</div>;

  return (
    <Layout>
      <div className="card p-4">
        <table className="table">
          <thead>
            <tr>
              <th>Table</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {tables.map(t => (
              <tr key={t.id}>
                <td>{t.number}</td>
                <td style={{ color: statusColors[t.status] }}>
                  {t.status}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}

export default Tables;
