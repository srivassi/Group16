"use client"; // ✅ Convert to Client Component

import React, { useEffect } from 'react';
import "./About.css";
import { Card, CardContent, CardMedia, Typography, Box } from '@mui/material';
import { useInView } from 'react-intersection-observer';

// ✅ Use public image paths (no import needed)
const christineImage = "/christine.jpg";
const andreImage = "/andre.jpg";
const siddhiImage = "/siddhi.jpg";
const alexImage = "/alex.jpg";

type TeamMemberProps = {
  member: {
    name: string;
    role: string;
    image: string;
    description: string;
  };
  index: number;
};

const TeamMember: React.FC<TeamMemberProps> = ({ member, index }) => {
    const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.2 });

    return (
        <Box
            ref={ref}
            className="team-section"
            sx={{
                display: 'flex',
                alignItems: 'center',
                flexDirection: index % 2 === 0 ? 'row' : 'row-reverse',
                opacity: inView ? 1 : 0,
                transform: inView ? 'translateX(0)' : (index % 2 === 0 ? 'translateX(-100px)' : 'translateX(100px)'),
                transition: 'opacity 0.8s ease-out, transform 0.8s ease-out',
                marginBottom: '40px',
            }}
        >
            <Card sx={{ minWidth: 225, maxWidth: 300, margin: 2 }}>
                <CardMedia component='img' alt={member.name} image={member.image} />
                <CardContent sx={{ backgroundColor: '#C0C0C0' }}>
                    <Typography variant="h5">{member.name}</Typography>
                    <Typography variant="subtitle1">{member.role}</Typography>
                </CardContent>
            </Card>

            <Box
                className="description-box"
                sx={{
                    maxWidth: '400px',
                    padding: '16px',
                    backgroundColor: '#F7F7F7',
                    borderRadius: '8px',
                    boxShadow: '0px 4px 6px rgba(0,0,0,0.1)',
                    marginLeft: index % 2 === 0 ? '20px' : '0px',
                    marginRight: index % 2 === 0 ? '0px' : '20px',
                }}
            >
                <Typography variant="body1">{member.description}</Typography>
            </Box>
        </Box>
    );
};

export default function AboutUs() {
    const teamMembers = [
        { name: 'Christine', role: 'Backend Developer', image: christineImage, description: "Hi! I'm Christine and I'm a SF Computer Science and Business student at Trinity. I have experience in Java, Python, React, SQL and Flask. Always looking for new and unique opportunities to grow my skillset!" },
        { name: 'Andre', role: 'AI Lead/ Backend Developer', image: andreImage, description: "A Computing Student from National College Of Ireland. I am a junior developer with a robust foundation in Web Development and Artificial Intelligence." },
        { name: 'Siddhi', role: 'UI Designer / Frontend Developer / Backend Developer', image: siddhiImage, description: "I am a Computer Science student with experience in NextJS, Typescript, Python, Java, Flask, HTML/CSS/JS and MongoDB. I am always eager to connect with brilliant young minds so reach out to me on LinkedIn and let's get a coffee :)" },
        { name: 'Alex', role: 'Frontend Developer', image: alexImage, description: "3rd Year Computer Science Student with experience in networking, web development and computer hardware" },
    ];

    useEffect(() => {
        const header = document.querySelector('.meet-the-team-header');
        if (header) {
            header.classList.add('visible');
        }
    }, []);

    return (
        <div className="about-us-container pt-24">
            <h1 className="meet-the-team-header">Meet the Team!</h1>
            <br />
            {teamMembers.map((member, index) => (
                <TeamMember key={index} member={member} index={index} />
            ))}
        </div>
    );
}
