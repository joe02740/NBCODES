import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function TableOfContents() {
  const [toc, setToc] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('https://nbcodes-47957a1fe60e.herokuapp.com/table_of_contents')
      .then(response => {
        setToc(response.data);
      })
      .catch(error => {
        console.error('Error fetching table of contents:', error);
        setError('Failed to load table of contents. Please try again later.');
      });
  }, []);

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (toc.length === 0) {
    return <div>Loading table of contents...</div>;
  }

  return (
    <div className="table-of-contents">
      <h1>New Bedford City Codes - Table of Contents</h1>
      {toc.map(chapter => (
        <div key={chapter._id} className="chapter">
          <h2>Chapter {chapter._id || 'General'}</h2>
          {chapter.sections.map(section => (
            <div key={section.Section} className="section">
              <h3>Section {section.Section || 'General'}</h3>
              {section.subsections.map(subsection => (
                <div key={subsection.Subsection} className="subsection">
                  <h4>Subsection {subsection.Subsection || 'General'}</h4>
                  <ul>
                    {subsection.items.map(item => (
                      <li key={item.NodeId}>
                        <Link to={`/ordinance/${item.NodeId}`}>
                          {item.Title} {item.Subtitle ? `- ${item.Subtitle}` : ''}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

export default TableOfContents;